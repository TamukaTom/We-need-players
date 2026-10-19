from django.urls import path

from . import views

urlpatterns = [
    path("", views.team_list, name="team_list"),
    path("team/<int:pk>/", views.team_report, name="team_report"),
    path("leagues/", views.league_list, name="league_list"),
    path("league/<slug:slug>/", views.league_detail, name="league_detail"),
]