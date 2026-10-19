from django.urls import path

from . import views

urlpatterns = [
    path("", views.team_list, name="team_list"),
    path("team/<int:pk>/", views.team_report, name="team_report"),
    path("leagues/", views.league_list, name="league_list"),
    path("league/<slug:slug>/", views.league_detail, name="league_detail"),
    path("players/", views.player_list, name="player_list"),
    path("player/<int:pk>/", views.player_detail, name="player_detail"),
]