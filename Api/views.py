import random
from django.db.models import query
import numpy
from django.http import Http404
from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from Api.serializers import *
from Api.models import *
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from Api.permissions import *
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.shortcuts import redirect


def przetasowanie(lista):
    wynik = [lista[0]]
    for n in range(len(lista) - 1):
        if n == 0:
            wynik.append(lista[-1])
        else:
            wynik.append(lista[n])
    return wynik


class ProfileViewSetList(APIView):
    queryset = Profile.objects.none()
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'
    post_permission = 'IsNotAuthorised'
    options_permission = 'IsAdmin'

    def get(self, format=None):
        queryset = Profile.objects.all().order_by('id')
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSetDetail(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'
    put_permission = 'IsAdmin'
    post_permission = 'IsNotAuthorised'
    patch_permission = 'IsOwner'
    delete_permission = 'IsOwner'
    options_permission = 'IsAdmin'

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ProfileSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ProfileSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        self.check_object_permissions(self.request, queryset)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        self.check_object_permissions(self.request, queryset)
        serializer = ProfileSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JudgeViewSetList(APIView):
    queryset = Judge.objects.none()
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'
    post_permission = 'IsAdmin'


    def get(self, format=None):
        queryset = Judge.objects.all()
        serializer = JudgeSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JudgeRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JudgeViewSetDetail(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'
    put_permission = 'IsAdmin'
    post_permission = 'IsAdmin'
    patch_permission = 'IsOwner'
    delete_permission = 'IsOwner'
    options_permission = 'IsAdmin'

    def get_object(self, pk):
        try:
            return Judge.objects.get(pk=pk)
        except Judge.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = JudgeSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = JudgeSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        self.check_object_permissions(self.request, queryset)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        self.check_object_permissions(self.request, queryset)
        serializer = JudgeSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TournamentViewSetList(APIView):
    queryset = TournamentInfo.objects.none()
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'
    post_permission = 'IsJudge'

    def get(self, format=None):
        queryset = TournamentInfo.objects.all().order_by('id')
        serializer = TournamentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TournamentSaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TournamentViewSetDetail(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'
    put_permission = 'IsJudge'
    post_permission = 'IsJudge'
    patch_permission = 'IsJudge'
    delete_permission = 'IsJudge'
    options_permission = 'IsAdmin'

    def get_object(self, pk):
        try:
            return TournamentInfo.objects.get(pk=pk)
        except TournamentInfo.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = TournamentSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = TournamentSaveSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = TournamentSaveSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameViewSetList(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'
    post_permission = 'IsJudge'

    def get(self, format=None):
        queryset = Game.objects.all().order_by('id')
        serializer = GameSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameViewSetDetail(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'
    put_permission = 'IsJudge'
    post_permission = 'IsJudge'
    patch_permission = 'IsJudge'
    delete_permission = 'IsJudge'
    options_permission = 'IsAdmin'

    def get_object(self, pk):
        try:
            return Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = GameSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = GameSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = GameSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            data = serializer.validated_data()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClubViewSetList(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsJudge'
    post_permission = 'IsJudge'

    def get(self, format=None):
        queryset = Club.objects.all().order_by('id')
        serializer = ClubSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClubSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClubViewSetDetail(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsJudge'
    put_permission = 'IsJudge'
    post_permission = 'IsJudge'
    patch_permission = 'IsJudge'
    delete_permission = 'IsJudge'
    options_permission = 'IsAdmin'

    def get_object(self, pk):
        try:
            return Club.objects.get(pk=pk)
        except Club.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ClubSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ClubSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ClubSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryViewSetList(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'
    post_permission = 'IsJudge'

    def get(self, format=None):
        queryset = Gallery.objects.all().order_by('id')
        serializer = GallerySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GallerySaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryViewSetDetail(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'
    put_permission = 'IsJudge'
    post_permission = 'IsJudge'
    patch_permission = 'IsJudge'
    delete_permission = 'IsJudge'
    options_permission = 'IsAdmin'

    def get_object(self, pk):
        try:
            return Gallery.objects.get(pk=pk)
        except Gallery.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = GallerySerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = GallerySaveSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = GallerySaveSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageViewSetList(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'
    post_permission = 'IsJudge'

    def get(self, format=None):
        queryset = Image.objects.all().order_by('id')
        serializer = ImageSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageViewSetDetail(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'
    put_permission = 'IsJudge'
    post_permission = 'IsJudge'
    patch_permission = 'IsJudge'
    delete_permission = 'IsJudge'
    options_permission = 'IsAdmin'

    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ImageSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ImageSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ImageSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TournamentNotificationViewSetList(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsJudge'
    post_permission = 'IsJudge'

    def get(self, format=None):
        queryset = TournamentNotification.objects.all().order_by('id')
        serializer = TournamentNotificationSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TournamentNotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TournamentNotificationViewSetDetail(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsNotificationOwner'
    put_permission = 'IsJudge'
    post_permission = 'IsJudge'
    patch_permission = 'IsJudge'
    delete_permission = 'IsNotificationOwner'
    options_permission = 'IsAdmin'

    def get_object(self, pk):
        try:
            return TournamentNotification.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        self.check_object_permissions(self.request, queryset)
        serializer = TournamentNotificationSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = TournamentNotificationSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        self.check_object_permissions(self.request, queryset)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = TournamentNotificationSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerInTournamentResultViewSetList(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'
    post_permission = 'IsJudge'
    options_permission = 'IsAdmin'

    def get(self, format=None):
        queryset = PlayerInTournamentResult.objects.all().order_by('id')
        serializer = PlayerInTournamentResultSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlayerInTournamentResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerInTournamentResultViewSetDetail(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'
    put_permission = 'IsJudge'
    post_permission = 'IsJudge'
    patch_permission = 'IsJudge'
    delete_permission = 'IsJudge'
    options_permission = 'IsAdmin'

    def get_object(self, pk):
        try:
            return PlayerInTournamentResult.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = PlayerInTournamentResultSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = PlayerInTournamentResultSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = PlayerInTournamentResultSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSetList(APIView):
    queryset = CustomUser.objects.none()
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'
    post_permission = 'IsNotAuthorised'

    def get(self, format=None):
        queryset = CustomUser.objects.all().order_by('-date_joined')
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserProfileSaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSetDetail(APIView):
    queryset = CustomUser.objects.none()
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'
    put_permission = 'IsAdmin'
    post_permission = 'IsNotAuthorised'
    patch_permission = 'IsOwner'
    delete_permission = 'IsOwner'
    options_permission = 'IsAdmin'

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = UserSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = UserUpdateSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = UserUpdateSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtainView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    serializer_class = TokenObtainSerializer


class PlayerGamesViewSetList(APIView):
    queryset = Profile.objects.none()
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'
    post_permission = 'IsJudge'

    def get(self, format=None):
        queryset = Profile.objects.all().order_by('id')
        serializer = PlayerGamesSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlayerGamesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoundViewSetDetail(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'
    post_permission = 'IsJudge'
    options_permission = 'IsAdmin'

    def get_object(self, pk):
        try:
            tournament = TournamentInfo.objects.filter(pk=pk)[0]
            return Round.objects.all().filter(tournament=tournament)
        except Round.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = RoundSerializer(queryset, many=True)
        return Response(serializer.data)


class RoundViewSetList(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'

    def get(self, format=None):
        queryset = Round.objects.all().order_by('id')
        serializer = RoundSerializer(queryset, many=True)
        return Response(serializer.data)


class TournamentPlayerResultViewSetDetail(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'
    options_permission = 'IsAdmin'

    def get_object(self, pk):
        try:
            return TournamentInfo.objects.get(pk=pk)
        except TournamentInfo.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = TournamentPlayerResultSerializer(queryset)
        return Response(serializer.data)


class TournamentPlayerResultViewSetList(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'

    def get(self, format=None):
        queryset = TournamentInfo.objects.all().order_by('id')
        serializer = TournamentPlayerResultSerializer(queryset, many=True)
        return Response(serializer.data)


class TournamentPlayerNotificationsViewSetList(APIView):
    permission_classes = (ApiPermissions,)
    get_permission = 'IsAuthorised'

    def get(self, format=None):
        queryset = TournamentInfo.objects.all().order_by('id')
        serializer = TournamentPlayerNotificationsSerializer(queryset, many=True)
        return Response(serializer.data)


class GenerateTournamentLadder(APIView):

    def get_object(self, pk):
        try:
            return TournamentInfo.objects.get(pk=pk)
        except TournamentInfo.DoesNotExist:
            raise Http404

    def przetasowanie(self, lista):
        wynik = [lista[0]]
        for n in range(len(lista) - 1):
            if n == 0:
                wynik.append(lista[-1])
            else:
                wynik.append(lista[n])
        return wynik

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = TournamentPlayerNotificationsSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        queryset = self.get_object(pk)
        notifications = TournamentNotification.objects.all().filter(tournament=pk)
        notification_number = notifications.count()
        notifications = list(notifications)
        random.shuffle(notifications)
        if not Game.objects.filter(tournament=queryset).exists():
            if queryset.play_type == 'LADDER':
                next_games = []
                rounds_number = int(numpy.ceil(numpy.log2(notification_number)))
                one_player = 2 ** rounds_number - notification_number
                gamesr1 = int((2 ** rounds_number) / 2)
                half_gamesr1 = gamesr1 / 2
                for r in range(rounds_number):
                    if r == 0:
                        curr_round = Round.objects.get_or_create(tournament=queryset, round_number=1)
                        for n in range(gamesr1):
                            if one_player > 0:
                                curr_round = Round.objects.get_or_create(tournament=queryset, round_number=1)
                                if half_gamesr1 > n >= (half_gamesr1 - int(one_player / 2)):
                                    player = random.choice(notifications)
                                    Game.objects.create(tournament=queryset, player1=player.player, player2=None,
                                                        round_number=curr_round, result='1')
                                    next_games.append(player)
                                    notifications.remove(player)
                                elif n >= half_gamesr1 and n >= (gamesr1 - int(one_player / 2) - 1):
                                    player = random.choice(notifications)
                                    Game.objects.create(tournament=queryset, player1=player.player, player2=None,
                                                        round_number=curr_round, result='1')
                                    next_games.append(player)
                                    notifications.remove(player)
                                else:
                                    if len(notifications) > 1:
                                        while True:
                                            player1 = random.choice(notifications)
                                            player2 = random.choice(notifications)
                                            if player1 != player2:
                                                break
                                        Game.objects.create(tournament=queryset, player1=player1.player,
                                                            player2=player2.player, round_number=curr_round, result='0')
                                        notifications.remove(player1)
                                        notifications.remove(player2)
                            else:
                                if len(notifications) > 0:
                                    while True:
                                        player1 = random.choice(notifications)
                                        player2 = random.choice(notifications)
                                        if player1 != player2:
                                            break
                                    Game.objects.create(tournament=queryset, player1=player1.player,
                                                        player2=player2.player, round_number=curr_round, result='0')
                                    notifications.remove(player1)
                                    notifications.remove(player2)
                    else:
                        next_games_number = len(next_games)  # 4
                        half_gamesr2 = 2 ** (rounds_number - r - 1) / 2
                        gamesr2 = numpy.ceil(2 ** (rounds_number - r - 1))
                        for n in range(2 ** (rounds_number - r - 1)):
                            if r == 1:
                                curr_round = Round.objects.get_or_create(tournament=queryset, round_number=2)
                                if next_games_number > 0:
                                    print(
                                        f'mniejsze {half_gamesr2} > {n} >= {half_gamesr2 - numpy.ceil(next_games_number / 4)}')
                                    print(
                                        f'wieksze {n} >= {half_gamesr2} and {n} >= {gamesr2 - numpy.ceil(next_games_number / 4)}')
                                    if half_gamesr2 > n >= half_gamesr2 - numpy.ceil(next_games_number / 4):
                                        if (len(next_games)) % 2 == 0:
                                            player1 = next_games[0]
                                            player2 = next_games[1]
                                            Game.objects.create(tournament=queryset, player1=player1.player,
                                                                player2=player2.player, round_number=curr_round,
                                                                result='0')
                                            next_games.pop(0)
                                            next_games.pop(0)
                                        else:
                                            player2 = next_games[0]
                                            Game.objects.create(tournament=queryset, player2=player2.player,
                                                                round_number=curr_round, result='0')
                                            next_games.pop(0)
                                    elif n >= half_gamesr2 and n >= (gamesr2 - numpy.ceil(next_games_number / 4)):
                                        if (len(next_games)) % 2 == 0:
                                            player1 = next_games[0]
                                            player2 = next_games[1]
                                            Game.objects.create(tournament=queryset, player1=player1.player,
                                                                player2=player2.player, round_number=curr_round,
                                                                result='0')
                                            next_games.pop(0)
                                            next_games.pop(0)
                                        else:
                                            player2 = next_games[0]
                                            Game.objects.create(tournament=queryset, player2=player2.player,
                                                                round_number=curr_round, result='0')
                                            next_games.pop(0)
                                    else:
                                        curr_round = Round.objects.get_or_create(tournament=queryset,
                                                                                 round_number=r + 1)
                                        Game.objects.create(tournament=queryset, round_number=curr_round, result='0')
                                else:
                                    curr_round = Round.objects.get_or_create(tournament=queryset, round_number=r + 1)
                                    Game.objects.create(tournament=queryset, round_number=curr_round, result='0')
                            else:
                                curr_round = Round.objects.get_or_create(tournament=queryset, round_number=r + 1)
                                Game.objects.create(tournament=queryset, round_number=curr_round, result='0')
            if queryset.play_type == 'RR':
                s = []
                if len(notifications) % 2 == 1:
                    notifications.append("")
                rounds_number = notification_number - 1
                for i in range(rounds_number):
                    if len(notifications) % 2 == 1:
                        notifications.append("")
                    mid = int(len(notifications) / 2)
                    lista1 = notifications[:mid]
                    lista2 = notifications[mid:]
                    lista2.reverse()
                    curr_round, created = Round.objects.get_or_create(tournament=queryset, round_number=i + 1)
                    print(curr_round)
                    for n in range(mid):
                        if lista1[n] == "":
                            Game.objects.create(tournament=queryset, player1=lista2[n].player, round_number=curr_round,
                                                result='1')
                        elif lista2[n] == "":
                            Game.objects.create(tournament=queryset, player1=lista1[n].player, round_number=curr_round,
                                                result='1')
                        else:
                            Game.objects.create(tournament=queryset, player1=lista1[n].player, player2=lista2[n].player,
                                                round_number=curr_round, result='0')
                        s.append([lista1[n], lista2[n]])
                    notifications = przetasowanie(notifications)

        return Response()

    def delete(self, request, pk):
        queryset = self.get_object(pk)
        games = Game.objects.filter(tournament=queryset)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class SectionViewSetList(APIView):

    def get(self, format=None):
        queryset = Section.objects.all().order_by('id')
        serializer = SectionSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SectionViewSetDetail(APIView):

    def get_object(self, pk):
        try:
            return Section.objects.get(pk=pk)
        except Section.DoesNotExist:
            raise Http404


    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = SectionSerializer(queryset)
        return Response(serializer.data)


    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = SectionSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = SectionSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        email = request.data.get('email', '')
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
            return Response({'Success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        return Response({'Error': 'Incorrect email'}, status=status.HTTP_200_OK)
        

class ChangePassword(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({'Error': 'Token is not valid, please, try again'})
        return Response ({'Success': True, 'message':'Credentials Valid', 'uidb64':uidb64, 'token':token})
    
    def patch(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
