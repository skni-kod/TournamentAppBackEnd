from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    rating = models.IntegerField(blank=True)
    country = models.CharField(max_length=60, blank=True)
    club = models.CharField(max_length=200, blank=True)
