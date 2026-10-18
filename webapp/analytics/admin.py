from django.contrib import admin

from .models import Player, Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "league", "attack_label", "defence_label", "midfield_label", "strength_display")
    list_filter = ("league", "attack_label", "defence_label", "midfield_label")
    search_fields = ("name",)

    @admin.display(description="Strength", ordering="strength")
    def strength_display(self, obj):
        return f"{obj.strength:.0f}"

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "team", "role", "age", "minutes", "score")
    list_filter = ("role", "team__league")
    search_fields = ("name", "team__name")
    ordering = ("-score",)