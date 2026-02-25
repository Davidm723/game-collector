from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Console(models.Model):
    name = models.CharField(max_length=100, unique=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    release_year = models.PositiveIntegerField(blank=True, null=True)
    image = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    console = models.ForeignKey(Console, on_delete=models.CASCADE, related_name="games")
    genres = models.ManyToManyField(Genre, related_name="games", blank=True)
    rawg_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    released = models.DateField(null=True, blank=True)
    image = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
