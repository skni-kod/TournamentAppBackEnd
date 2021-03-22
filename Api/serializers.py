from rest_framework import serializers
from .models import Player
from .models import Tournament


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'surname', 'rating', 'country', 'club')
class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('id', 'name', 'address', 'data', 'Maxparticipants', 'mincategory', 'maxcategory', 'gamesystem')
