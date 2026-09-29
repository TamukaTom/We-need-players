# We need players

A tool that analyses team and player stats from Europe's top 5 leagues (2025-26 season) to show where a team is strong, where it is weak, and why.

## What it does so far
- Cleans player stats and converts them to per-90-minute numbers
- Ranks players against others in the same position (percentiles)
- Builds team profiles and labels strengths and weaknesses
- Explains defensive problems using shots faced and goalkeeper save %

## Example finding
Manchester United score 1.74 goals per match (83rd percentile out of 96 teams) but concede 1.32 (64th percentile). The tool shows their defence is not the problem in front of goal: they allow only 3.6 shots on target per match (82nd percentile). The leak is at the last step, where their goalkeepers save 66% of shots faced, lower than about 80% of teams.

## Data
Player stats from this Kaggle dataset: https://www.kaggle.com/datasets/hubertsidorowicz/football-players-stats-2025-2026
The CSV is not included in this repository. Download it from Kaggle and place it in the project folder as `players_data-2025_2026.csv`.

## How to run
1. Install the libraries: `pip install -r requirements.txt`
2. Open `explore.ipynb` in VS Code or Jupyter
3. Run all cells

## Limitations
This dataset has no passing, possession or expected-goals stats, so the tool cannot yet judge passing or shot quality. Adding richer data is planned.

## Planned
- Player recommendations for a team's weak areas
- Richer data (passing, xG, possession)
- Web dashboard built with Django
- Automatic data updates