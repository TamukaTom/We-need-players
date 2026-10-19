from . import config
from .models import Player


def roles_needed(team):
    roles = (config.ATTACK_LABEL_TO_ROLES.get(team.attack_label, [])
             + config.DEFENCE_LABEL_TO_ROLES.get(team.defence_label, [])
             + config.MIDFIELD_LABEL_TO_ROLES.get(team.midfield_label, []))
    return list(dict.fromkeys(roles))  # remove repeats, keep order


def recommend(team, role, n=5, max_age=None, max_gap=None, max_club_gap=None,
              min_minutes=config.RECOMMEND_MIN_MINUTES):
    # The likely starters are the players in this role with the most minutes
    k = config.STARTERS_NEEDED.get(role, 1)
    squad = list(team.players.filter(role=role, score__isnull=False).order_by("-minutes")[:k])
    if not squad:
        return None
    weakest = min(squad, key=lambda p: p.score)

    pool = (Player.objects
            .filter(role=role, score__gt=weakest.score, minutes__gte=min_minutes)
            .exclude(team=team))
    if max_age is not None:
        pool = pool.filter(age__lte=max_age)
    if max_gap is not None:
        pool = pool.filter(score__lte=weakest.score + max_gap)
    if max_club_gap is not None:
        pool = pool.filter(team__strength__lte=team.strength + max_club_gap)

    candidates = list(pool.select_related("team").order_by("-score")[:n])
    for p in candidates:
        p.better_by = p.score - weakest.score
    return {"weakest": weakest, "candidates": candidates}