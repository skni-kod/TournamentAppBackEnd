from rest_framework import serializers
from .models import *


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'surname', 'rating', 'country', 'club')


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('id', 'name', 'address', 'data', 'Maxparticipants', 'mincategory', 'maxcategory', 'gamesystem')


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meet
        fields = ('id_meet', 'id_player', 'id_player1', 'result', 'date', 'round')
