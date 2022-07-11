from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10)
    premiere = models.DateTimeField("%Y-%m-%d")
    classification = models.IntegerField()
    synopsis = models.TextField()
    genres = models.ManyToManyField("genres.Genre", related_name="movies")
