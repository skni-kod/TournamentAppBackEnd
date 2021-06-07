from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static
from Api.views import *
from . import settings
from django.contrib.auth import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/profile/$', ProfileViewSetList.as_view(), name='Player_List'),
    url(r'^api/profile/(?P<pk>\d+)/$', ProfileViewSetDetail.as_view(), name='Player_Detail'),
    url(r'^api/judge/$', JudgeViewSetList.as_view(), name='Judge_List'),
    url(r'^api/judge/(?P<pk>\d+)/$', JudgeViewSetDetail.as_view(), name='Judge_Detail'),
    url(r'^api/tournament/$', TournamentViewSetList.as_view(), name='Tournament_List'),
    url(r'^api/tournament/(?P<pk>\d+)/$', TournamentViewSetDetail.as_view(), name='Tournament_Detail'),
    url(r'^api/club/$', ClubViewSetList.as_view(), name='Club_List'),
    url(r'^api/club/(?P<pk>\d+)/$', ClubViewSetDetail.as_view(), name='Club_Detail'),
    url(r'^api/image/$', ImageViewSetList.as_view(), name='Image_List'),
    url(r'^api/image/(?P<pk>\d+)/$', ImageViewSetDetail.as_view(), name='Image_Detail'),
    url(r'^api/gallery/$', GalleryViewSetList.as_view(), name='Gallery_List'),
    url(r'^api/gallery/(?P<pk>\d+)/$', GalleryViewSetDetail.as_view(), name='Gallery_Detail'),
    url(r'^api/game/$', GameViewSetList.as_view(), name='Game_List'),
    url(r'^api/game/(?P<pk>\d+)/$', GameViewSetDetail.as_view(), name='Game_Detail'),
    url(r'^api/tournament_notification/$', TournamentNotificationViewSetList.as_view(), name='Tournament_Notification_List'),
    url(r'^api/tournament_notification/(?P<pk>\d+)/$', TournamentNotificationViewSetDetail.as_view(), name='Tournament_Notification_Detail'),
    url(r'^api/player_result/$', PlayerInTournamentResultViewSetList.as_view(), name='Player_Result_List'),
    url(r'^api/player_result/(?P<pk>\d+)/$', PlayerInTournamentResultViewSetDetail.as_view(), name='Player_Result_Detail'),
    url(r'^api/user/(?P<pk>\d+)/$', UserViewSetDetail.as_view(), name='User_Detail'),
    url(r'^api/token/$', TokenObtainView.as_view(),name='token_obtain'),
    url(r'^api/token/refresh/$', TokenRefreshView.as_view(),name='token_refresh'),
    url(r'^api/user/$', UserViewSetList.as_view(), name='User_List'),
    url(r'^api/player_games/$', PlayerGamesViewSetList.as_view(), name='Player_games'),
    url(r'^api/tournament_games/(?P<pk>\d+)/$', TournamentGamesViewSetDetail.as_view(), name='Tournament_Games'),
    url(r'^api/tournament_games/$', TournamentGamesViewSetList.as_view(), name='Tournament_Games'),
    url(r'^api/tournament_player_result/(?P<pk>\d+)/$', TournamentPlayerResultViewSetDetail.as_view(), name='Tournament_Player_Result'),
    url(r'^api/tournament_player_result/$', TournamentPlayerResultViewSetList.as_view(), name='Tournament_Player_Result'),
    url(r'^api/tournament_player_notifications/$', TournamentPlayerNotificationsViewSetList.as_view(), name='Tournament_Player_Notifications'),
    url(r'^api/generate/(?P<pk>\d+)/$', GenerateTournamentLadder.as_view(), name='generate'),
    url('api-auth/', include('rest_framework.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
