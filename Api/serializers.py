from rest_framework import serializers
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

from .models import *


class UserSerializer(serializers.ModelSerializer):
    is_admin_user = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'profile', 'password',
                  'first_name', 'last_name', 'is_admin_user')
        read_only_fields = ('profile',)
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def get_is_admin_user(self, obj):
        return obj.is_staff

    def create(self,validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'profile', 'first_name', 'last_name')
        read_only_fields = ('profile',)


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'club_name', 'club_info', 'club_logo', 'country')


class ProfileWithoutUserSerializer(serializers.ModelSerializer):
    club = ClubSerializer()

    class Meta:
        model = Profile
        fields = ('id', 'category', 'rating', 'country', 'gender', 'club')


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
    user = UserSerializer(read_only=True)
    club = ClubSerializer()

    class Meta:
        model = Profile
        fields = ('id', 'user', 'rating', 'country', 'club')


class TournamentSerializer(serializers.ModelSerializer):
    gallery = GallerySerializer()

    class Meta:
        model = TournamentInfo
        fields = ('id', 'name', 'address', 'date', 'memberslimit', 'pairingsystem', 'organiser', 'playtype', 'winpoints', 'losepoints', 'drawpoints',
        'byepoints', 'country', 'mincategory', 'maxcategory', 'category', 'gallery')


class GameSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer()
    player1 = ProfileWithoutUserSerializer()
    player2 = ProfileWithoutUserSerializer()

    class Meta:
        model = Game
        fields = ('id', 'tournament', 'player1', 'player2', 'round_number', 'result', 'date')


class TournamentNotificationSerializer(serializers.ModelSerializer):
    player = ProfileSerializer()
    tournament = TournamentSerializer()

    class Meta:
        model = TournamentNotification
        fields = ('id', 'player', 'tournament')


class PlayerInTournamentResultSerializer(serializers.ModelSerializer):
    player = ProfileSerializer()
    tournament = TournamentSerializer()

    class Meta:
        model = PlayerInTournamentResult
        fields = ('id', 'pointsstatus', 'player', 'tournament')



