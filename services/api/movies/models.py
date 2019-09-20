from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=177) # 177 is the longest movie title in existence
    year = models.CharField(max_length=4)
    rated = models.CharField(max_length=5, null=True)
    released = models.DateField()
    runtime = models.IntegerField()
    genre = models.CharField(max_length=70, null=True)
    director = models.CharField(max_length=70)
    writer = models.CharField(max_length=255)
    actors = models.CharField(max_length=255)
    plot = models.TextField(null=True)
    language = models.CharField(max_length=255)
    country = models.CharField(max_length=47)
    awards = models.CharField(max_length=255, null=True)
    poster = models.URLField(null=True)
    metascore = models.IntegerField(null=True)
    imdbrating = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    imdbvotes = models.IntegerField(null=True)  # needs to be parsed from omdb i.e. "72,555"
    imdbid = models.CharField(max_length=40, null=True, unique=True)
    type = models.CharField(max_length=20, null=True)
    dvd = models.DateField(null=True)
    boxoffice = models.IntegerField(null=True)
    production = models.CharField(max_length=40, null=True)
    website = models.URLField(null=True)

class Comment(models.Model):
    value = models.TextField()
    movie = models.ForeignKey("Movie", related_name='comments', on_delete="cascade")

class Rating(models.Model):
    source = models.CharField(max_length=100)
    value = models.CharField(max_length=20)
    movie = models.ForeignKey("Movie", related_name='ratings', on_delete="cascade")
