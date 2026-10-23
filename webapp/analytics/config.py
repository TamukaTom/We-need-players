# Cut-offs and metric lists live here so they are easy to change.

MIN_MINUTES = 900  # players below this are not scored

# CSV column -> readable name
PLAYER_STATS = {
    "Gls": "Goals", "Ast": "Assists", "Sh": "Shots", "SoT": "ShotsOnTarget",
    "Int": "Interceptions", "TklW": "TacklesWon", "Crs": "Crosses",
    "Fls": "FoulsCommitted", "Fld": "FoulsDrawn", "Off": "Offsides",
}
LOWER_IS_BETTER = ["FoulsCommitted", "Offsides"]

TEAM_STATS = ["Goals", "Assists", "Shots", "ShotsOnTarget", "Interceptions",
              "TacklesWon", "Crosses", "FoulsCommitted", "Offsides", "GoalsConceded"]
TEAM_LOWER_IS_BETTER = ["FoulsCommitted", "Offsides", "GoalsConceded"]

ROLE_NAMES = {"FW": "Forward", "MF": "Midfielder", "DF": "Defender", "GK": "Goalkeeper"}

# Which percentiles are averaged into a player's score, per role
SCORE_STATS = {
    "Forward": ["Goals", "Assists", "Shots", "ShotsOnTarget"],
    "Attacking Midfielder": ["Goals", "Assists", "Shots", "ShotsOnTarget", "FoulsDrawn"],
    "Midfielder": ["Goals", "Assists", "TacklesWon", "Interceptions", "FoulsDrawn"],
    "Defender": ["TacklesWon", "Interceptions", "FoulsCommitted", "Assists"],
}

# Cut-offs used by the labels (percentiles, 0-100)
STRONG = 75  # top quarter counts as strong
MID = 50     # above or below average
LOW = 40     # below this counts as low

WEAK = 25  # at or below this counts as a weakness

STAT_LABELS = {
    "Goals": "Goals", "Assists": "Assists", "Shots": "Shots",
    "ShotsOnTarget": "Shots on target", "Interceptions": "Interceptions",
    "TacklesWon": "Tackles won", "Crosses": "Crosses",
    "FoulsCommitted": "Fouls committed", "Offsides": "Offsides",
    "GoalsConceded": "Goals conceded",
}

STARTERS_NEEDED = {"Goalkeeper": 1, "Defender": 4, "Midfielder": 2,
                   "Attacking Midfielder": 3, "Forward": 1}

RECOMMEND_MIN_MINUTES = 1800

# Which roles to look for, given each diagnosis label
ATTACK_LABEL_TO_ROLES = {
    "wasteful finishing": ["Forward"],
    "low chance creation": ["Attacking Midfielder"],
    "both": ["Forward", "Attacking Midfielder"],
}
DEFENCE_LABEL_TO_ROLES = {
    "gap in goal": ["Goalkeeper"],
    "problem in front of keeper": ["Defender"],
    "both": ["Goalkeeper", "Defender"],
}
MIDFIELD_LABEL_TO_ROLES = {
    "ball winning": ["Midfielder"],
    "creation": ["Attacking Midfielder"],
    "both": ["Midfielder", "Attacking Midfielder"],
}

STAT_LABELS["FoulsDrawn"] = "Fouls drawn"

UNDERPERFORMER_BELOW = 40  # players scoring below this are listed as lowest-rated