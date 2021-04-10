from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Club(models.Model):
    id_club = models.IntegerField(primary_key=True)
    club_name = models.CharField(max_length=50)
    club_info = models.TextField(max_length=500,blank=True)
    club_logo = models.ImageField(upload_to='club_logo/')
    country = models.CharField(max_length=60,blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    category = models.CharField(max_length=20)
    rating = models.IntegerField(blank=True, validators=[MinValueValidator(0)])
    country = models.CharField(max_length=60, blank=True)
    gender = models.CharField(max_length=6, choices=(('M', 'Male'), ('F', 'Female')))
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING, many=False)
    email = models.EmailField()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Gallery(models.Model):
    name = models.CharField(max_length=20)


class Image(models.Model):
    file = models.ImageField(upload_to='/images')
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, many=True)


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
    gallery = models.OneToOneField(Gallery, on_delete=models.CASCADE)


class Game(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, many=False)
    player1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='+')
    player2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='+')
    round_number = models.IntegerField()
    date = models.DateTimeField
    result = models.CharField(max_length=20, choices=(('P1W', f'{player1} won'), ('P1W', f'{player2} won')))


