from django.db.models.query import QuerySet
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *

from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


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
            email=validated_data['email'], group='Players'
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'profile', 'first_name', 'last_name')
        read_only_fields = ('profile',)


class ShortUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')


class ShortProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'country', 'rating')


class ShortProfileWithClubSerializer(CountryFieldMixin, serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    club_name = serializers.CharField(source="club.club_name")
    club_id = serializers.IntegerField(source="club.id")

    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'country', 'rating', 'club_id', 'club_name')


class ProfileForGameSerializer(CountryFieldMixin, serializers.ModelSerializer):
    user = ShortUserSerializer()

    class Meta:
        model = Profile
        fields = ('id', 'user', 'rating', 'country', 'club')


class ClubListSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'club_name', 'club_info_short', 'country')


class ClubDetailSerializer(CountryFieldMixin, serializers.ModelSerializer):
    members = ShortProfileSerializer(many=True, source='profile')

    class Meta:
        model = Club
        fields = ('id', 'club_name', 'club_info', 'club_logo', 'country', 'members')


class ProfileWithoutUserSerializer(CountryFieldMixin, serializers.ModelSerializer):
    club = ClubDetailSerializer()

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


class ProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    is_judge = serializers.SerializerMethodField()
    club_id = serializers.IntegerField(source='club.id')
    club_name = serializers.CharField(source='club.club_name', allow_null=True)

    class Meta:
        model = Profile
        fields = ('id', 'email', 'first_name', 'last_name', 'is_judge', 'rating', 'country', 'club_id', 'club_name')

    def get_is_judge(self, obj):
        return obj.user.groups.filter(name='Judges').exists()


class JudgeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Judge
        fields = ('id', 'user', 'judge_category')


class JudgeSaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Judge
        fields = ('id', 'user', 'judge_category')


class TournamentListSerializer(CountryFieldMixin, serializers.ModelSerializer):

    class Meta:
        model = TournamentInfo
        fields = ('id', 'name', 'play_type', 'country')


class TournamentDetailSerializer(CountryFieldMixin, serializers.ModelSerializer):
    gallery = GallerySerializer()

    class Meta:
        model = TournamentInfo
        fields = (
            'id', 'name', 'address', 'date', 'members_limit', 'organiser', 'play_type', 'win_points',
            'lose_points', 'draw_points',
            'bye_points', 'country', 'gallery', 'judge')


class ShortTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentInfo
        fields = ('id', 'name')


class GameSerializer(serializers.ModelSerializer):
    tournament = ShortTournamentSerializer()
    player1 = ShortProfileSerializer()
    player2 = ShortProfileSerializer()
    round_number = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ('id', 'tournament', 'player1', 'player2', 'result', 'round_number')

    def get_round_number(self, obj):
        return obj.round_number.round_number


class TNSerializer(serializers.ModelSerializer):
    player = ShortProfileWithClubSerializer()

    class Meta:
        model = TournamentNotification
        fields = ('id', 'player')


class TournamentNotificationSerializer(serializers.ModelSerializer):
    player = ShortProfileWithClubSerializer()
    tournament = ShortTournamentSerializer()

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


class RoundSerializer(serializers.ModelSerializer):
    game = GameSerializer(many=True)

    class Meta:
        model = Round
        fields = ('id', 'round_number', 'game')


class TokenObtainSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, CustomUser):
        token = super(TokenObtainSerializer,cls).get_token(CustomUser)

        token['email'] = CustomUser.email

        return token

    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(TokenObtainSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'id': self.user.id})
        # and everything else you want to send in the response
        return data


class JudgeRegisterSerializer(serializers.ModelSerializer):
    is_admin_user = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ( 'id','email', 'profile', 'password',
                  'first_name', 'last_name', 'is_admin_user')
        read_only_fields = ('profile',)
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def get_is_admin_user(self, obj):
        return obj.is_staff

    def create(self,validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'], group='Judges',
        )
        user.set_password(validated_data['password'])
        user.perm = True
        user.save()
        judge = Judge(user=user, judge_category=500)
        judge.save()
        return user


class TournamentPlayerResultSerializer(serializers.ModelSerializer):
    result = PlayerInTournamentResultSerializer(many=True, source='player_results')

    class Meta:
        model = TournamentInfo
        fields = ('id', 'result')


class TournamentPlayerNotificationsSerializer(serializers.ModelSerializer):
    notification = TNSerializer(many=True, source='notifications')

    class Meta:
        model = TournamentInfo
        fields = ('id', 'notification')


class TournamentSaveSerializer(CountryFieldMixin, serializers.ModelSerializer):

    class Meta:
        model = TournamentInfo
        fields = (
            'id', 'name', 'address', 'date', 'members_limit', 'organiser', 'play_type', 'win_points',
            'lose_points', 'draw_points',
            'bye_points', 'country', 'gallery', 'judge')


class GallerySaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gallery
        fields = ()


class ProfileForRegistrationSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('gender', 'country', 'club')


class UserProfileSaveSerializer(serializers.ModelSerializer):
    profile = ProfileForRegistrationSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name', 'profile')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = CustomUser.objects.create(**validated_data)
        for pr in profile_data:
            Profile.objects.create(user=user, **pr, rating=0)
        return user


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'title', 'text')



class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=18, write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        password = attrs.get('password')
        token = attrs.get('token')
        uidb64 = attrs.get('uidb64')

        id = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise AuthenticationFailed('The reset link is invalid', 401)

        user.set_password(password)
        user.save()

        return (user)

