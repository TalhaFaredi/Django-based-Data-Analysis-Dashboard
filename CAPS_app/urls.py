from django.urls import path
from CAPS_app import views , t20views

urlpatterns = [
    path('', views.index, name='index'),
     path("dashboard/",views.dashboard , name="dashboard"),
    path("Toss/", views.Toss , name ="Toss"),
    path('decision/', views.decision, name='decision'),
    path('team_stats/', views.team_stats, name='team_stats'),
    path('team_against_team/', views.team_stats, name='team_against_team'),
    path('team-against-venue/', views.team_stats, name='team_against_venue'),
    path("t20Analysis/", t20views.t20_analysis, name='t20Analysis'),
    path("t20stats/", t20views.team_stats, name='t20stats'),
    path("team_selectt20", t20views.team_stats, name='team_selectt20'),
    path("team_vs_team_t20", t20views.team_stats, name='team_vs_team_t20'),
    path("regestration" , views.register_view, name='Registration')
]