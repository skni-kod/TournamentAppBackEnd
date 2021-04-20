from datetime import datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from sorl.thumbnail import ImageField


class Club(models.Model):
    club_name = models.CharField(max_length=50)
    club_info = models.TextField(max_length=500,blank=True)
    club_logo = models.ImageField(upload_to='club_logo/', blank=True)
    country = models.CharField(max_length=60,blank=True)

    def __str__(self):
        return self.club_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    category = models.CharField(max_length=20, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=60, blank=True)
    gender = models.CharField(max_length=6, choices=(('M', 'Male'), ('F', 'Female')), blank=True)
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Gallery(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "galleries"


class Image(models.Model):
    image = ImageField(upload_to='images/')
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, default=None, related_name='image')

    def __str__(self):
        return f'{self.gallery.name} {self.id}'

class TournamentInfo(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.today(), validators=[MinValueValidator(timezone.now())])
    memberslimit = models.IntegerField(blank=True, validators=[MinValueValidator(2)], default=2)
    PAIRING = (
        ('random', 'random'),
        ('netherland', 'netherland'),
        ('monrad', 'monrad'),
    )
    pairingsystem = models.CharField(choices=PAIRING, max_length= 20, default="RANDOM")
    organiser = models.CharField(max_length=200)
    CHOICES = (
        ('RR', 'round-robin'),
        ('LABEL', 'label'),
        ('GROUPS', 'groups'),
    )
    playtype = models.CharField(choices=CHOICES, max_length= 20, default="RR")
    winpoints = models.FloatField(validators=[MinValueValidator(0)], default=2)
    losepoints = models.FloatField(validators=[MinValueValidator(0)], default=0)
    drawpoints = models.FloatField(validators=[MinValueValidator(0)], default=1)
    byepoints = models.FloatField(validators=[MinValueValidator(0)], default=0.5)
    country = models.CharField(blank=True, max_length=200)
    mincategory = models.IntegerField(blank=True, validators=[MinValueValidator(0)], default=0)
    maxcategory = models.IntegerField(blank=True, validators=[MinValueValidator(0)], default=2000)
    CATEGORIES = (
        ('men', 'men'),
        ('women', 'women'),
        ('mixed', 'mixed'),
    )
    category = models.CharField(choices=CATEGORIES, max_length= 10, default="mixed")
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, blank=True, related_name='tournament')

    def __str__(self):
        return self.name


class Game(models.Model):
    tournament = models.ForeignKey(TournamentInfo, on_delete=models.CASCADE, related_name='tournament')
    player1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='player2')
    round_number = models.IntegerField()
    date = models.DateTimeField(blank=True, null=True)
    result = models.CharField(max_length=20, blank=True, choices=(('P1W', f'{player1} won'), ('P1W', f'{player2} won')))

    def __str__(self):
        return f'{self.player1} vs {self.player2}'


class TournamentNotification(models.Model):
    player = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notifications')
    tournament = models.ForeignKey(TournamentInfo, on_delete=models.CASCADE, related_name='notifications')

    def __str__(self):
        return f'{self.player} {self.tournament}'


class PlayerInTournamentResult(models.Model):
    pointsstatus = models.FloatField(default=0)
    player = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='player_results')
    tournament = models.ForeignKey(TournamentInfo, on_delete=models.CASCADE, related_name='player_results')


