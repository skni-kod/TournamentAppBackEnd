from django.db import models
from datetime import datetime
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
    

class Player(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    rating = models.IntegerField(blank=True)
    country = models.CharField(max_length=60, blank=True)
    club = models.CharField(max_length=200, blank=True)

class Tournament(models.Model):
    name = models.CharField(max_length=200)
    address =  models.CharField(max_length=200)
    data = models.DateTimeField(blank = True, default = datetime.today(), validators=[MinValueValidator(timezone.now())])
    Maxparticipants = models.IntegerField(null=True, validators=[MinValueValidator(2)])
    mincategory = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    maxcategory = models.IntegerField(validators=[MinValueValidator(0)], default=2000)
    RR = 'RR'
    LABEL = 'LABEL'
    CHOICES = (
        (RR, ('round-robin')),
        (LABEL, ('label')),
    )
    gamesystem = models.CharField(choices = CHOICES, max_length= 20, default="RR")