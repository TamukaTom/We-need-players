from django.urls import path

from . import views

urlpatterns = [
    path("", views.team_list, name="team_list"),
    path("team/<int:pk>/", views.team_report, name="team_report"),
]