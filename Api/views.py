import random
from django.contrib.auth import authenticate, login
from django.db.models.fields import EmailField
from django.http.response import HttpResponse

import numpy
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import PasswordField
from Api.serializers import *
from Api.models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from Api.permissions import *
from Api.decorators import method_permission_classes

class ProfileViewSetList(APIView):
    queryset = Profile.objects.none()

    def get(self, format=None):
        queryset = Profile.objects.all()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    @method_permission_classes((IsNotAuthorised or IsReadOnly,))
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSetDetail(APIView):

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ProfileSerializer(queryset)
        return Response(serializer.data)

    @method_permission_classes((IsNotAuthorised,))
    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ProfileSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsAdmin,))
    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @method_permission_classes((IsProfileOwner or IsReadOnly,))
    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ProfileSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TournamentViewSetList(APIView):
    queryset = TournamentInfo.objects.none()

    @method_permission_classes((IsJudge or IsReadOnly, IsAuthorised,))
    def get(self, format=None):
        queryset = TournamentInfo.objects.all()
        serializer = TournamentSerializer(queryset, many=True)
        return Response(serializer.data)

    @method_permission_classes((IsJudge,))
    def post(self, request):
        serializer = TournamentSaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TournamentViewSetDetail(APIView):

    @method_permission_classes((IsJudge or IsReadOnly, IsAuthorised,))
    def get_object(self, pk):
        try:
            return TournamentInfo.objects.get(pk=pk)
        except TournamentInfo.DoesNotExist:
            raise Http404

    @method_permission_classes((IsJudge or IsReadOnly,))
    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = TournamentSerializer(queryset)
        return Response(serializer.data)

    @method_permission_classes((IsJudge,))
    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = TournamentSaveSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsTournamentJudge,))
    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @method_permission_classes((IsTournamentJudge,))
    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = TournamentSaveSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameViewSetList(APIView):

    @method_permission_classes((IsGameJudge or IsReadOnly, IsAuthorised,))
    def get(self, format=None):
        queryset = Game.objects.all()
        serializer = GameSerializer(queryset, many=True)
        return Response(serializer.data)

    @method_permission_classes((IsGameJudge,))
    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameViewSetDetail(APIView):

    @method_permission_classes((IsGameJudge or IsReadOnly, IsAuthorised,))
    def get_object(self, pk):
        try:
            return Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise Http404

    @method_permission_classes((IsGameJudge or IsReadOnly, IsAuthorised,))
    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = GameSerializer(queryset)
        return Response(serializer.data)

    @method_permission_classes((IsGameJudge,))
    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = GameSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsGameJudge,))
    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @method_permission_classes((IsGameJudge,))
    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = GameSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClubViewSetList(APIView):

    @method_permission_classes((IsAuthorised, IsReadOnly))
    def get(self, format=None):
        queryset = Club.objects.all()
        serializer = ClubSerializer(queryset, many=True)
        return Response(serializer.data)

    @method_permission_classes((IsAuthorised, IsReadOnly))
    def post(self, request):
        serializer = ClubSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClubViewSetDetail(APIView):

    @method_permission_classes((IsAuthorised, IsReadOnly))
    def get_object(self, pk):
        try:
            return Club.objects.get(pk=pk)
        except Club.DoesNotExist:
            raise Http404

    @method_permission_classes((IsAuthorised, IsReadOnly))
    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ClubSerializer(queryset)
        return Response(serializer.data)

    @method_permission_classes((IsAdmin,))
    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ClubSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsAdmin,))
    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @method_permission_classes((IsAdmin,))
    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ClubSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryViewSetList(APIView):

    @method_permission_classes((IsJudge or IsReadOnly, IsAuthorised,))
    def get(self, format=None):
        queryset = Gallery.objects.all()
        serializer = GallerySerializer(queryset, many=True)
        return Response(serializer.data)

    @method_permission_classes((IsJudge,))
    def post(self, request):
        serializer = GallerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryViewSetDetail(APIView):

    @method_permission_classes((IsJudge or IsReadOnly, IsAuthorised,))
    def get_object(self, pk):
        try:
            return Gallery.objects.get(pk=pk)
        except Gallery.DoesNotExist:
            raise Http404

    @method_permission_classes((IsJudge or IsReadOnly, IsAuthorised,))
    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = GallerySerializer(queryset)
        return Response(serializer.data)
    
    @method_permission_classes((IsJudge,))
    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = GallerySerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsJudge,))
    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @method_permission_classes((IsJudge,))
    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = GallerySerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageViewSetList(APIView):

    @method_permission_classes((IsJudge or IsReadOnly, IsAuthorised,))
    def get(self, format=None):
        queryset = Image.objects.all()
        serializer = ImageSerializer(queryset, many=True)
        return Response(serializer.data)

    @method_permission_classes((IsJudge,))
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageViewSetDetail(APIView):

    @method_permission_classes((IsJudge or IsReadOnly, IsAuthorised,))
    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    @method_permission_classes((IsJudge or IsReadOnly, IsAuthorised,))
    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ImageSerializer(queryset)
        return Response(serializer.data)

    @method_permission_classes((IsJudge,))
    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ImageSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsJudge,))
    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @method_permission_classes((IsJudge,))
    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = ImageSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TournamentNotificationViewSetList(APIView):

    @method_permission_classes((IsAuthorised,))
    def get(self, format=None):
        queryset = TournamentNotification.objects.all()
        serializer = TournamentNotificationSerializer(queryset, many=True)
        return Response(serializer.data)

    @method_permission_classes((IsAuthorised, IsPlayer,))
    def post(self, request):
        serializer = TournamentNotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TournamentNotificationViewSetDetail(APIView):
    permission_classes = (IsAuthorised,)

    def get_object(self, pk):
        try:
            return TournamentNotification.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    @method_permission_classes((IsPlayer,))
    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = TournamentNotificationSerializer(queryset)
        return Response(serializer.data)

    @method_permission_classes((IsPlayer,))
    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = TournamentNotificationSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsNotificationOwner,))
    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @method_permission_classes((IsNotificationOwner,))
    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = TournamentNotificationSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerInTournamentResultViewSetList(APIView):

    @method_permission_classes((IsResultJudge or IsReadOnly,))
    def get(self, format=None):
        queryset = PlayerInTournamentResult.objects.all()
        serializer = PlayerInTournamentResultSerializer(queryset, many=True)
        return Response(serializer.data)

    @method_permission_classes((IsResultJudge,))
    def post(self, request):
        serializer = PlayerInTournamentResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerInTournamentResultViewSetDetail(APIView):

    @method_permission_classes((IsResultJudge or IsReadOnly,))
    def get_object(self, pk):
        try:
            return PlayerInTournamentResult.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    @method_permission_classes((IsResultJudge or IsReadOnly,))
    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = PlayerInTournamentResultSerializer(queryset)
        return Response(serializer.data)

    @method_permission_classes((IsResultJudge,))
    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = PlayerInTournamentResultSerializer(queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsResultJudge,))
    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @method_permission_classes((IsResultJudge,))
    def patch(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = PlayerInTournamentResultSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSetDetail(APIView):
    queryset = CustomUser.objects.none()

    @method_permission_classes((IsReadOnly,))
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    @method_permission_classes((IsReadOnly,))
    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = UserSerializer(queryset)
        return Response(serializer.data)

    @method_permission_classes((IsNotAuthorised,))
    def put(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = UserUpdateSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsAdmin,))
    def delete(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @method_permission_classes((IsReadOnly or IsUserOwner,))
    def patch(self, request,  pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = UserUpdateSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSetList(APIView):
    queryset = CustomUser.objects.none()

    def get(self, format=None):
        queryset = CustomUser.objects.all().order_by('-date_joined')
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @method_permission_classes((IsNotAuthorised or IsReadOnly,))
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtainView(TokenObtainPairView):

    permission_classes = (AllowAny,)

    serializer_class = TokenObtainSerializer

class TestView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, format=None):
        queryset = CustomUser.objects.all()
        serializer = UserSerializer(queryset,many=True)
        return Response(serializer.data)

      
class PlayerGamesViewSetList(APIView):
    permission_classes = (IsAuthorised,)
    queryset = Profile.objects.none()

    def get(self, format=None):
        queryset = Profile.objects.all()
        serializer = PlayerGamesSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlayerGamesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TournamentGamesViewSetDetail(APIView):
    permission_classes = (IsAuthorised,)

    def get_object(self, pk):
        try:
            return TournamentInfo.objects.get(pk=pk)
        except TournamentInfo.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        queryset = self.get_object(pk)
        serializer = TournamentGamesSerializer(queryset)
        return Response(serializer.data)


class TournamentGamesViewSetList(APIView):
    permission_classes = (IsAuthorised,)

    def get(self, format=None):
        queryset = TournamentInfo.objects.all()
        serializer = TournamentGamesSerializer(queryset, many=True)
        return Response(serializer.data)


class TournamentPlayerResultViewSetDetail(APIView):
    permission_classes = (IsAuthorised,)

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
    permission_classes = (IsAuthorised,)

    def get(self, format=None):
        queryset = TournamentInfo.objects.all()
        serializer = TournamentPlayerResultSerializer(queryset, many=True)
        return Response(serializer.data)


class TournamentPlayerNotificationsViewSetList(APIView):
    permission_classes = (IsAuthorised,)

    def get(self, format=None):
        queryset = TournamentInfo.objects.all()
        serializer = TournamentPlayerNotificationsSerializer(queryset, many=True)
        return Response(serializer.data)


class GenerateTournamentLadder(APIView):
    permission_classes = (IsAuthorised, IsJudge)

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
                rounds_number = int(numpy.ceil(numpy.log2(notification_number)))
                one_player = 2 ** rounds_number - notification_number
                gamesr1 = int((2 ** rounds_number) / 2)
                half_gamesr1 = gamesr1 / 2
                for r in range(rounds_number):
                    if r == 0:
                        for n in range(gamesr1):
                            if one_player > 0:
                                if half_gamesr1 > n >= (half_gamesr1 - int(one_player/2)):
                                    player = random.choice(notifications)
                                    Game.objects.create(tournament=queryset, player1=player.player, player2=None, round_number=1, result='1')
                                    notifications.remove(player)
                                    print('mniejsze')
                                elif n >= half_gamesr1 and n >= (gamesr1-int(one_player/2)-1):
                                    player = random.choice(notifications)
                                    Game.objects.create(tournament=queryset, player1=player.player, player2=None, round_number=1, result='1')
                                    notifications.remove(player)
                                    print('wieksze')
                                else:
                                    if len(notifications) > 1:
                                        while True:
                                            player1 = random.choice(notifications)
                                            player2 = random.choice(notifications)
                                            if player1 != player2:
                                                break
                                        Game.objects.create(tournament=queryset, player1=player1.player, player2=player2.player, round_number=1, result='0')
                                        notifications.remove(player1)
                                        notifications.remove(player2)
                                        print('podwojne')
                                print('koniec')
                            else:
                                if len(notifications) > 0:
                                    while True:
                                        player1 = random.choice(notifications)
                                        player2 = random.choice(notifications)
                                        if player1 != player2:
                                            break
                                    Game.objects.create(tournament=queryset, player1=player1.player, player2=player2.player, round_number=1, result='0')
                                    notifications.remove(player1)
                                    notifications.remove(player2)
                    else:
                        for n in range(2**(r-1)):
                            Game.objects.create(tournament=queryset, round_number=r+1, result='0')

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
                    for n in range(mid):
                        if lista1[n] == "":
                            Game.objects.create(tournament=queryset, player1=lista2[n].player, round_number=1, result='1')
                        elif lista2[n] == "":
                            Game.objects.create(tournament=queryset, player1=lista1[n].player, round_number=1, result='1')
                        else:
                            Game.objects.create(tournament=queryset, player1=lista1[n].player, player2=lista2[n].player,  round_number=1, result='1')
                        s.append([lista1[n], lista2[n]])
                    notifications = self.przetasowanie(notifications)
        return Response()

    def delete(self, request, pk):
        queryset = self.get_object(pk)
        games = Game.objects.filter(tournament=queryset)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
