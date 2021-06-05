from datetime import datetime

from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework import permissions
from sorl.thumbnail import ImageField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group

"""CUSTOM USER MODEL"""


class CustomUserManager(BaseUserManager):
    def _create_user(self, email,group, password=None, **extra_fields):
        """Tworzenie i zapisywanie usera z podanym mailem i hasłem"""""
        if not email:
            raise ValueError('No email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        group_add = Group.objects.get(name='Players')
        user.groups.add(group_add)
        user.save(using=self._db)
        return user

    def create_user(self, email,group,password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, group,password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Tworzenie i zapisywanie superusera z podanym mailem i hasłem"""""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
    def __str__(self):
        return self.email


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


"##################################################################"


class Club(models.Model):
    club_name = models.CharField(max_length=255)
    club_info = models.TextField(max_length=500, blank=True)
    club_logo = models.ImageField(upload_to='club_logo/', blank=True)
    country = models.CharField(max_length=60)

    def __str__(self):
        return self.club_name


class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='profile')
    category = models.CharField(max_length=20, blank=True)
    rating = models.SmallIntegerField(default=0)
    country = models.CharField(max_length=60)
    gender = models.CharField(max_length=1, choices=(('M', 'M'), ('F', 'F')), blank=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Judge(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='judge')
    judge_category = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Judge {self.user.first_name} {self.user.last_name}'


class Gallery(models.Model):

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "galleries"


class Image(models.Model):
    image = ImageField(upload_to='images/')
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='image')

    def __str__(self):
        return f'{self.gallery.id} {self.id}'


class TournamentInfo(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField()
    members_limit = models.IntegerField(validators=[MinValueValidator(2)], default=2)
    organiser = models.CharField(max_length=200, blank=True)
    CHOICES = (
        ('RR', 'round-robin'),
        ('LADDER', 'ladder'),
        ('GROUPS', 'groups'),
    )
    play_type = models.CharField(choices=CHOICES, max_length=20, default="RR")
    win_points = models.FloatField(validators=[MinValueValidator(0)], default=2)
    lose_points = models.FloatField(validators=[MinValueValidator(0)], default=0)
    draw_points = models.FloatField(validators=[MinValueValidator(0)], default=1)
    bye_points = models.FloatField(validators=[MinValueValidator(0)], default=0.5)
    country = models.CharField(max_length=60)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, blank=True, related_name='tournament', null=True)
    judge = models.ForeignKey(Judge, on_delete=models.CASCADE, related_name='judge', null=True)

    def __str__(self):
        return self.name


class PlayerInTournamentResult(models.Model):
    points_status = models.FloatField(default=0)
    player = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='player')
    tournament = models.ForeignKey(TournamentInfo, on_delete=models.CASCADE, related_name='player_results')

    def __str__(self):
        return f'{self.player} w {self.tournament}'


class Game(models.Model):
    tournament = models.ForeignKey(TournamentInfo, on_delete=models.CASCADE, related_name='tournament')
    player1 = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True, related_name='player1')
    player2 = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True, related_name='player2')
    results = (('0', 'Match not yet played'),
               ('1', f'{player1} Won'),
               ('2', f'{player2} Won'),
               ('3', 'Tie'),
               ('4', f'{player1} Won by bye'),
               ('5', f'{player2} Won by bye'))
    round_number = models.IntegerField()
    result = models.CharField(max_length=20, blank=True, choices=results)

    def __str__(self):
        return f'{self.player1} vs {self.player2}'


class TournamentNotification(models.Model):
    player = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notifications')
    tournament = models.ForeignKey(TournamentInfo, on_delete=models.CASCADE, related_name='notifications')

    def __str__(self):
        return f'{self.player} {self.tournament}'
