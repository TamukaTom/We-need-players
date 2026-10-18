import pandas as pd

from . import config, rules


def build_team_table(df):
    """One row per team: totals, per-match numbers, and percentiles across all teams.
    A high percentile always means 'good'."""
    team = df.groupby(["Squad", "Comp"]).agg(
        Goals=("Gls", "sum"),
        Assists=("Ast", "sum"),
        Shots=("Sh", "sum"),
        ShotsOnTarget=("SoT", "sum"),
        Interceptions=("Int", "sum"),
        TacklesWon=("TklW", "sum"),
        Crosses=("Crs", "sum"),
        FoulsCommitted=("Fls", "sum"),
        Offsides=("Off", "sum"),
        GoalsConceded=("GA", "sum"),
        TotalPlayer90s=("90s", "sum"),
    ).reset_index()
    team["Matches"] = (team["TotalPlayer90s"] / 11).round()

    keeper = df[df["Pos"] == "GK"].groupby(["Squad", "Comp"]).agg(
        ShotsOnTargetFaced=("SoTA", "sum"),
        Saves=("Saves", "sum"),
    ).reset_index()
    team = team.merge(keeper, on=["Squad", "Comp"], how="left")

    for s in config.TEAM_STATS:
        team[s + "_permatch"] = team[s] / team["Matches"]
        pct = team[s + "_permatch"].rank(pct=True) * 100
        team[s + "_permatch_percentile"] = 100 - pct if s in config.TEAM_LOWER_IS_BETTER else pct

    team["ShotsOnTargetFaced_permatch"] = team["ShotsOnTargetFaced"] / team["Matches"]
    team["ShotsOnTargetFaced_permatch_percentile"] = 100 - team["ShotsOnTargetFaced_permatch"].rank(pct=True) * 100
    team["SavePercent"] = team["Saves"] / team["ShotsOnTargetFaced"] * 100
    team["SavePercent_percentile"] = team["SavePercent"].rank(pct=True) * 100

    team["GoalsPerShotOnTarget"] = team["Goals"] / team["ShotsOnTarget"]
    team["GoalsPerShotOnTarget_percentile"] = team["GoalsPerShotOnTarget"].rank(pct=True) * 100

    team["BallWinning_percentile"] = (team["TacklesWon_permatch_percentile"] + team["Interceptions_permatch_percentile"]) / 2
    team["Creation_percentile"] = team["Assists_permatch_percentile"]

    team["GoalDiffPerMatch"] = (team["Goals"] - team["GoalsConceded"]) / team["Matches"]
    team["Strength_percentile"] = team["GoalDiffPerMatch"].rank(pct=True) * 100

    team["AttackLabel"] = team.apply(rules.attack_label, axis=1)
    team["DefenceLabel"] = team.apply(rules.defence_label, axis=1)
    team["MidfieldLabel"] = team.apply(rules.midfield_label, axis=1)
    return team

def build_player_table(df):
    """Players with enough minutes: role, per-90 stats, percentiles within role, and a score."""
    players = df[df["Min"] >= config.MIN_MINUTES].copy()

    def role(pos):
        if pos == "MF,FW":
            return "Attacking Midfielder"
        return config.ROLE_NAMES.get(pos.split(",")[0], pos)

    players["Role"] = players["Pos"].apply(role)

    for short, name in config.PLAYER_STATS.items():
        col = name + "_per90"
        players[col] = players[short] / players["90s"]
        pct = players.groupby("Role")[col].rank(pct=True) * 100
        players[col + "_percentile"] = 100 - pct if name in config.LOWER_IS_BETTER else pct

    def outfield_score(row):
        stats = config.SCORE_STATS.get(row["Role"])
        if stats is None:
            return float("nan")
        return sum(row[s + "_per90_percentile"] for s in stats) / len(stats)

    players["Score"] = players.apply(outfield_score, axis=1)

    is_gk = players["Role"] == "Goalkeeper"
    keepers = players[is_gk]
    save_pct = keepers["Save%"].rank(pct=True) * 100
    goals_against = 100 - keepers["GA90"].rank(pct=True) * 100
    clean_sheets = keepers["CS%"].rank(pct=True) * 100
    players.loc[is_gk, "Score"] = (save_pct + goals_against + clean_sheets) / 3
    return players