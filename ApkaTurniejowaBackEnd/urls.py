from django.contrib import admin
from django.conf.urls import url
from Api.views import *
from Spotkania.views import *



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/player/$', PlayerViewSetList.as_view(), name='Player_List'),
    url(r'^api/player/(?P<pk>\d+)/$', PlayerViewSetDetail.as_view(), name='Player_Detail'),
    url(r'^spotkania/$', MeetingViewSetList.as_view(), name='Meeting_List'),
    url(r'^spotkania/(?P<pk>\d+)/$', MeetingViewSetDetail.as_view(), name='Meeting_Detail'),
]
