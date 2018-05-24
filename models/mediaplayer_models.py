from django.db import models

class Movie(models.Model):
    AC = 'AC'
    DR = 'DR'
    HR = 'HR'
    CO = 'CO'
    FA = 'FA'
    AD = 'AD'
    title = models.CharField(max_length=50)
    logo = models.FileField()
    movie_link = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    GENRE = (
        (AC, 'Action'),
        (DR, 'Drama'),
        (HR, 'Horror'),
        (CO, 'Comedy'),
        (FA, 'Fantasy'),
        (AD, 'Adults'),
    )
    movie_genre = models.CharField(
        max_length=2,
        choices=GENRE,
        default=AC
    )

    class Meta:
        db_table = "Movie"

    def __str__(self):
        return self.title
