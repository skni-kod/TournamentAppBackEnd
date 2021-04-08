from rest_framework import serializers
from .models import *


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'surname', 'rating', 'country', 'club')


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('id', 'name', 'address', 'date', 'memberslimit', 'mincategory', 'maxcategory', 'pairingsystem', 'organiser', 'playtype', 'winpoints', 'losepoints', 'drawpoints',
        'byepoints', 'country', 'category')


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meet
        fields = ('id_meet', 'id_player', 'id_player1', 'result', 'date', 'round')

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id_club','club_name','club_info','club_logo','country')