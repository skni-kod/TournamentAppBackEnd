from rest_framework import serializers
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

from .models import *


class UserSerializer(serializers.ModelSerializer):
    is_admin_user = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'profile', 'password',
                  'first_name', 'last_name', 'is_admin_user')
        read_only_fields = ('profile', 'groups')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'club_name', 'club_info', 'club_logo', 'country')


class ProfileWithoutUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        club = ClubSerializer
        fields = ('id', 'category', 'rating', 'country', 'gender', 'club' )


class ImageSerializer(serializers.ModelSerializer):
    thumbnail = HyperlinkedSorlImageField(
        '512x512',
        options={'crop': 'center'},
        source='image',
        read_only='true'
    )

    class Meta:
        model = Image
        fields = ('id', 'gallery', 'image', 'thumbnail')


class GallerySerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=True)

    class Meta:
        model = Gallery
        fields = ('id', 'name', 'image')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        club = ClubSerializer
        fields = ('id', 'first_name', 'surname', 'rating', 'country', 'club')


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentInfo
        gallery = GallerySerializer
        fields = ('id', 'name', 'address', 'date', 'memberslimit', 'pairingsystem', 'organiser', 'playtype', 'winpoints', 'losepoints', 'drawpoints',
        'byepoints', 'country', 'mincategory', 'maxcategory', 'category', 'gallery')


class GameSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer
    player1 = ProfileSerializer
    player2 = ProfileSerializer

    class Meta:
        model = Game
        fields = ('id', 'tournament', 'player1', 'player2', 'round_number', 'result', 'date')



class TournamentNotificationSerializer(serializers.ModelSerializer):
    player = ProfileSerializer
    tournament = TournamentSerializer
    class Meta:
        fields = ('id', 'player', 'tournament')


class PlayerInTournamentResultSerializer(serializers.ModelSerializer):
    player = ProfileSerializer
    tournament = TournamentSerializer
    class Meta:
        fields = ('id', 'pointsstatus', 'player', 'tournament')
