from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'channel'

urlpatterns = [
    path("myUploads", login_required(myuploads), name='myuploads'),
    path("channel", channel, name='channel_view'),  # colocar o nome do canal aqui dps
    path("playlist", playlist, name='playlist_view'),
    path("about/<int:cod>", about, name='about_view'),
    path("uploads", uploads, name='uploads_view'),
    path("similar", similar, name='similar_view')
]
