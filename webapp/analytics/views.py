from django.shortcuts import get_object_or_404, render
from collections import Counter

from django.http import Http404
from django.utils.text import slugify
from . import config, recommend, rules
from .models import Team


def _int_param(request, name, default):
    """Read a whole number from the address (?max_age=25), or fall back to the default."""
    try:
        return int(request.GET.get(name, ""))
    except ValueError:
        return default


def team_list(request):
    query = request.GET.get("q", "").strip()
    teams = Team.objects.all()
    if query:
        teams = teams.filter(name__icontains=query)
    teams = teams.order_by("league", "name")
    return render(request, "analytics/team_list.html", {"teams": teams, "query": query})


def team_report(request, pk):
    team = get_object_or_404(Team, pk=pk)

    row = {
        "Squad": team.name,
        "AttackLabel": team.attack_label,
        "DefenceLabel": team.defence_label,
        "MidfieldLabel": team.midfield_label,
        **team.metrics,
    }
    explanations = [
        ("Attack", rules.explain_attack(row).split(": ", 1)[-1]),
        ("Defence", rules.explain_defence(row).split(": ", 1)[-1]),
        ("Midfield", rules.explain_midfield(row).split(": ", 1)[-1]),
    ]

    rows = []
    for stat in config.TEAM_STATS:
        pct = team.metrics.get(stat + "_permatch_percentile")
        if pct is None:
            continue
        if pct >= config.STRONG:
            tag = "strength"
        elif pct <= config.WEAK:
            tag = "weakness"
        else:
            tag = "average"
        rows.append({
            "name": config.STAT_LABELS.get(stat, stat),
            "value": team.metrics[stat + "_permatch"],
            "percentile": pct,
            "width": round(pct),
            "tag": tag,
        })
    rows.sort(key=lambda r: r["percentile"], reverse=True)

    max_age = _int_param(request, "max_age", 27)
    max_gap = _int_param(request, "max_gap", 40)
    max_club_gap = _int_param(request, "max_club_gap", 20)

    suggestions = []
    for role in recommend.roles_needed(team):
        result = recommend.recommend(team, role, max_age=max_age,
                                     max_gap=max_gap, max_club_gap=max_club_gap)
        if result:
            suggestions.append({"role": role, **result})

    context = {
        "team": team,
        "club_level": round(team.strength),
        "explanations": explanations,
        "rows": rows,
        "suggestions": suggestions,
        "max_age": max_age,
        "max_gap": max_gap,
        "max_club_gap": max_club_gap,
    }
    return render(request, "analytics/team_report.html", context)

SORT_FIELDS = {
    "name": "name",
    "level": "-strength",
    "attack": "attack_label",
    "defence": "defence_label",
    "midfield": "midfield_label",
}


def _leagues():
    leagues = []
    for name in Team.objects.order_by("league").values_list("league", flat=True).distinct():
        display = name.split(" ", 1)[-1]
        leagues.append({"league": name, "display": display, "slug": slugify(display)})
    return leagues


def league_list(request):
    leagues = []
    for lg in _leagues():
        leagues.append({**lg, "count": Team.objects.filter(league=lg["league"]).count()})
    return render(request, "analytics/league_list.html", {"leagues": leagues})


def league_detail(request, slug):
    league = next((lg for lg in _leagues() if lg["slug"] == slug), None)
    if league is None:
        raise Http404("Unknown league")

    all_teams = Team.objects.filter(league=league["league"])
    labels = {
        "attack": Counter(all_teams.values_list("attack_label", flat=True)),
        "defence": Counter(all_teams.values_list("defence_label", flat=True)),
        "midfield": Counter(all_teams.values_list("midfield_label", flat=True)),
    }

    teams = all_teams
    selected = {}
    for area in ("attack", "defence", "midfield"):
        value = request.GET.get(area, "")
        selected[area] = value
        if value:
            teams = teams.filter(**{area + "_label": value})

    sort = request.GET.get("sort", "level")
    if sort not in SORT_FIELDS:
        sort = "level"
    teams = teams.order_by(SORT_FIELDS[sort], "name")

    keep = request.GET.copy()
    keep.pop("sort", None)

    context = {
        "league": league,
        "teams": teams,
        "total": all_teams.count(),
        "summary": [(area.title(), labels[area].most_common()) for area in labels],
        "options": {area: sorted(labels[area]) for area in labels},
        "selected": selected,
        "sort": sort,
        "base_qs": keep.urlencode(),
    }
    return render(request, "analytics/league_detail.html", context)