from rest_framework import serializers
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

from .models import *


class UserSerializer(serializers.ModelSerializer):
    is_admin_user = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'profile', 'password',
                  'first_name', 'last_name', 'is_admin_user')
        read_only_fields = ('profile',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_is_admin_user(self, obj):
        return obj.is_staff

    def create(self, validated_data):
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


class ShortUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')


class ProfileForGameSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()

    class Meta:
        model = Profile
        fields = ('id', 'user', 'rating', 'country', 'club')


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
        fields = ('id', 'image')


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
        fields = (
            'id', 'name', 'address', 'date', 'members_limit', 'pairing_system', 'organiser', 'play_type', 'win_points',
            'lose_points', 'draw_points',
            'bye_points', 'country', 'gallery', 'judge')


class ShortTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentInfo
        fields = ('id', 'name')


class GameSerializer(serializers.ModelSerializer):
    tournament = ShortTournamentSerializer()
    player1 = ProfileForGameSerializer()
    player2 = ProfileForGameSerializer()

    class Meta:
        model = Game
        fields = ('id', 'tournament', 'player1', 'player2', 'round_number', 'result')


class TournamentNotificationSerializer(serializers.ModelSerializer):
    player = ProfileSerializer()
    tournament = TournamentSerializer()

    class Meta:
        model = TournamentNotification
        fields = ('id', 'player', 'tournament')


class PlayerGamesSerializer(serializers.ModelSerializer):
    game1 = GameSerializer(many=True, source='player1')
    game2 = GameSerializer(many=True, source='player2')
    user = ShortUserSerializer()

    class Meta:
        model = Profile
        fields = ('id', 'user', 'game1', 'game2')


class PlayerInTournamentResultSerializer(serializers.ModelSerializer):
    player_games = PlayerGamesSerializer(source='player')
    tournament = ShortTournamentSerializer()

    class Meta:
        model = PlayerInTournamentResult
        fields = ('id', 'points_status', 'tournament', 'player_games')


class TournamentGamesSerializer(serializers.ModelSerializer):
    game = GameSerializer(many=True, source='tournament')

    class Meta:
        model = TournamentInfo
        fields = ('id', 'game')


class TournamentPlayerResultSerializer(serializers.ModelSerializer):
    result = PlayerInTournamentResultSerializer(many=True, source='player_results')

    class Meta:
        model = TournamentInfo
        fields = ('id', 'result')
