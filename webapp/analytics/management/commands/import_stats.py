from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from analytics import config, pipeline
from analytics.models import Player, Team


def clean(value):
    """Turn numpy numbers into plain floats, and NaN into None (JSON cannot store NaN)."""
    if value is None or pd.isna(value):
        return None
    return float(value)


class Command(BaseCommand):
    help = "Read the player stats CSV, compute the analysis, and save it to the database"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to players_data-2025_2026.csv")

    def handle(self, *args, **options):
        path = Path(options["csv_path"])
        if not path.exists():
            raise CommandError(f"File not found: {path}")

        df = pd.read_csv(path)
        self.stdout.write(f"Loaded {len(df)} player rows")

        team_df = pipeline.build_team_table(df)
        player_df = pipeline.build_player_table(df)

        team_metric_cols = [c for c in team_df.columns
                            if c.endswith("_permatch") or c.endswith("_percentile")]
        team_metric_cols += ["SavePercent", "GoalsPerShotOnTarget", "GoalDiffPerMatch"]

        player_stat_cols = [c for c in player_df.columns
                            if c.endswith("_per90") or c.endswith("_per90_percentile")]
        player_stat_cols += ["Save%", "GA90", "CS%"]

        with transaction.atomic():
            # Re-running the import replaces the old data instead of duplicating it
            Player.objects.all().delete()
            Team.objects.all().delete()

            Team.objects.bulk_create([
                Team(
                    name=row["Squad"],
                    league=row["Comp"],
                    matches=int(row["Matches"]),
                    strength=clean(row["Strength_percentile"]),
                    attack_label=row["AttackLabel"],
                    defence_label=row["DefenceLabel"],
                    midfield_label=row["MidfieldLabel"],
                    metrics={c: clean(row[c]) for c in team_metric_cols},
                )
                for _, row in team_df.iterrows()
            ])
            teams = {(t.name, t.league): t for t in Team.objects.all()}

            Player.objects.bulk_create([
                Player(
                    name=row["Player"],
                    team=teams[(row["Squad"], row["Comp"])],
                    role=row["Role"],
                    age=None if pd.isna(row["Age"]) else int(row["Age"]),
                    minutes=int(row["Min"]),
                    score=clean(row["Score"]),
                    stats={c: clean(row[c]) for c in player_stat_cols},
                )
                for _, row in player_df.iterrows()
            ])

        self.stdout.write(self.style.SUCCESS(
            f"Saved {Team.objects.count()} teams and {Player.objects.count()} players"))

        utd = Team.objects.get(name="Manchester Utd")
        self.stdout.write(f"Utd labels: {utd.attack_label} / {utd.defence_label} / {utd.midfield_label}")
        best = Player.objects.filter(role="Forward").order_by("-score").first()
        self.stdout.write(f"Top forward in the database: {best.name} ({best.team.name}) {best.score:.2f}")