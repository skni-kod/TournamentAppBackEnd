from django.db import models
from datetime import datetime
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Player(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    rating = models.IntegerField(blank=True, validators=[MinValueValidator(0)])
    country = models.CharField(max_length=60, blank=True)
    club = models.CharField(max_length=200, blank=True)


class Tournament(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.today(), validators=[MinValueValidator(timezone.now())])
    memberslimit = models.IntegerField(blank=True, validators=[MinValueValidator(2)])
    mincategory = models.IntegerField(blank=True, validators=[MinValueValidator(0)], default=0)
    maxcategory = models.IntegerField(blank=True, validators=[MinValueValidator(0)], default=2000)
    RANDOM = 'random'
    NETHERLAND = 'netherland'
    MONRAD = 'monrad'
    PAIRING = (
        (RANDOM, 'random'),
        (NETHERLAND, 'netherland'),
        (MONRAD, 'monrad'),
    )
    pairingsystem = models.CharField(choices=PAIRING, max_length= 20, default="RANDOM")
    organiser = models.CharField(max_length=200)
    RR = 'RR'
    LABEL = 'LABEL'
    GROUPS = 'groups'
    CHOICES = (
        (RR, 'round-robin'),
        (LABEL, 'label'),
        (GROUPS, 'groups'),
    )
    playtype = models.CharField(choices=CHOICES, max_length= 20, default="RR")
    winpoints = models.FloatField(validators=[MinValueValidator(0)], default=2)
    losepoints = models.FloatField(validators=[MinValueValidator(0)], default=0)
    drawpoints = models.FloatField(validators=[MinValueValidator(0)], default=1)
    byepoints = models.FloatField(validators=[MinValueValidator(0)], default=0.5)
    country = models.CharField(blank=True, max_length=200)
    MEN = 'men'
    WOMEN = 'women'
    MIXED = 'mixed'
    CATEGORIES = (
        (MEN, 'men'),
        (WOMEN, 'women'),
        (MIXED, 'mixed'),
    )
    category = models.CharField(choices=CATEGORIES, max_length= 10, default="mixed")



class Meet(models.Model):
    id_meet = models.IntegerField(primary_key=True)
    id_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='+')
    id_player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='+')
    result = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)])
    date = models.DateTimeField()
    round = models.IntegerField()

    
class Club(models.Model):
    id_club = models.IntegerField(primary_key=True)
    club_name = models.CharField(max_length=50)
    club_info = models.TextField(max_length=500,blank=True)
    club_logo = models.ImageField(upload_to='club_logo/')
    country = models.CharField(max_length=60,blank=True)
