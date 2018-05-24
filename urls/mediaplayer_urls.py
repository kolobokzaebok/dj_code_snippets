from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('player/<int:movie_id>', views.play_video, name='player'),
]

