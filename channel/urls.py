from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'channel'

urlpatterns = [
    path("myUploads", login_required(myuploads), name='myuploads'),
    path("<int:cod>", channel, name='channel_view'),
    path("playlist/<int:cod>", playlist, name='playlist_view'),
    path("about/<int:cod>", about, name='about_view'),
    path("uploads/<int:cod>,", uploads, name='uploads_view')
]
