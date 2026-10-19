from django.shortcuts import get_object_or_404, render

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