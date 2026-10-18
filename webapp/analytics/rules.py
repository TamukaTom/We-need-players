from . import config


def attack_label(row):
    goals = row["Goals_permatch_percentile"]
    volume = row["ShotsOnTarget_permatch_percentile"]
    conversion = row["GoalsPerShotOnTarget_percentile"]
    if goals >= config.STRONG:
        return "strong attack"
    elif volume >= config.MID and conversion < config.LOW:
        return "wasteful finishing"
    elif volume < config.MID and conversion >= config.MID:
        return "low chance creation"
    elif volume < config.MID and conversion < config.MID:
        return "both"
    return "average attack"


def defence_label(row):
    conceded = row["GoalsConceded_permatch_percentile"]
    faced = row["ShotsOnTargetFaced_permatch_percentile"]
    saves = row["SavePercent_percentile"]
    if conceded >= config.STRONG:
        return "strong defence"
    elif faced >= config.MID and saves < config.LOW:
        return "gap in goal"
    elif faced < config.MID and saves >= config.MID:
        return "problem in front of keeper"
    elif faced < config.MID and saves < config.MID:
        return "both"
    return "average defence"


def midfield_label(row):
    defence_strong = row["GoalsConceded_permatch_percentile"] >= config.STRONG
    attack_strong = row["Goals_permatch_percentile"] >= config.STRONG
    weak_ball_winning = row["BallWinning_percentile"] < config.LOW and not defence_strong
    weak_creation = row["Creation_percentile"] < config.LOW and not attack_strong
    if weak_ball_winning and weak_creation:
        return "both"
    elif weak_ball_winning:
        return "ball winning"
    elif weak_creation:
        return "creation"
    return "no midfield concern"


def explain_attack(row):
    name = row["Squad"]
    label = row["AttackLabel"]
    if label == "strong attack":
        if row["ShotsOnTarget_permatch_percentile"] >= config.STRONG and row["GoalsPerShotOnTarget_percentile"] < config.MID:
            return f"{name}: strong attack built on volume. They test the keeper more than most teams, but convert fewer of those shots than an average team."
        return f"{name}: strong attack, scoring more than most teams."
    if label == "wasteful finishing":
        return f"{name}: tests the keeper often, but converts fewer shots on target than most teams."
    if label == "low chance creation":
        return f"{name}: converts shots at a decent rate, but does not create enough shots on target."
    if label == "both":
        return f"{name}: creates few shots on target and converts fewer of them than most teams."
    return f"{name}: attack is around league average, nothing stands out."


def explain_defence(row):
    name = row["Squad"]
    label = row["DefenceLabel"]
    if label == "strong defence":
        return f"{name}: strong defence, concedes fewer goals than most teams."
    if label == "gap in goal":
        return f"{name}: limits shots on target, but concedes more than the best defences. The gap is in goal, where saves are below most teams."
    if label == "problem in front of keeper":
        return f"{name}: opponents get plenty of shots on target, so the problem is in front of the keeper, not in goal."
    if label == "both":
        return f"{name}: allows many shots on target and saves fewer than most teams, so the problem is both."
    return f"{name}: no clear defensive problem in this data."


def explain_midfield(row):
    name = row["Squad"]
    label = row["MidfieldLabel"]
    if label == "ball winning":
        return f"{name}: wins fewer tackles and interceptions than most teams, and the defence is not strong enough to explain it as style."
    if label == "creation":
        return f"{name}: records fewer assists than most teams, and the attack is not strong enough to explain it."
    if label == "both":
        return f"{name}: low on both ball winning and assists, with no strong attack or defence to offset it."
    return f"{name}: no clear midfield concern in this data."