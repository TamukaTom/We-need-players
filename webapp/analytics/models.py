from django.db import models
from django.utils.text import slugify


class Team(models.Model):
    name = models.CharField(max_length=100)
    league = models.CharField(max_length=50)
    matches = models.PositiveSmallIntegerField()
    strength = models.FloatField(help_text="Goal difference per match, ranked 0-100 across all teams")
    attack_label = models.CharField(max_length=40)
    defence_label = models.CharField(max_length=40)
    midfield_label = models.CharField(max_length=40)
    badge_url = models.URLField(blank=True)
    metrics = models.JSONField(default=dict)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["name", "league"], name="unique_team_per_league"),
        ]

    def __str__(self):
        return f"{self.name} ({self.league})"

    @property
    def league_display(self):
        # "eng Premier League" -> "Premier League"
        return self.league.split(" ", 1)[-1]

    @property
    def league_slug(self):
        # "Premier League" -> "premier-league", used in web addresses
        return slugify(self.league_display)


class Player(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players")
    role = models.CharField(max_length=30)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    minutes = models.PositiveIntegerField()
    score = models.FloatField(null=True, blank=True)
    photo_url = models.URLField(blank=True)
    stats = models.JSONField(default=dict)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["role", "score"])]

    def __str__(self):
        return f"{self.name} ({self.team.name})"