from rest_framework import serializers
from .models import Meet

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meet
        fields = ('id_meet', 'id_player', 'id_player1', 'result', 'date', 'round')
