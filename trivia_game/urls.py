# trivia_game/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_question/', views.add_question, name='add_question'),
    path('play_game/', views.play_game, name='play_game'),
    path('play_question/', views.play_question, name='play_question'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('load-data/', load_data_view, name='load_data'),

]
