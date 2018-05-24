import subprocess
from django.views import generic
from .models import Movie
from django.shortcuts import redirect


class IndexView(generic.ListView):
    template_name = 'movies/index.html'
    context_object_name = 'movie_list'

    def get_queryset(self):
        return Movie.objects.all()


def play_video(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    subprocess.Popen(["C:/Program Files/VideoLAN/VLC/vlc.exe", movie.movie_link])

    return redirect('movies:index')
