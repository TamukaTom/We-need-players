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