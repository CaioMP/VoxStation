from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'channel'

urlpatterns = [
    path("myUploads", login_required(myuploads), name='myuploads'),
    path("<str:nome>/", channel, name='channel_view'),
    path("playlist/<str:nome>", playlist, name='playlist_view'),
    path("about/<str:nome>", about, name='about_view'),
    path("uploads/<str:nome>", uploads, name='uploads_view'),
    path("partner/<str:nome>", partner, name='partner_view'),
    path("follow/<str:nome>", follow, name="follow_view"),
    path("playlist_all", playlist_all, name='playlist_all_view'),  # colocar o nome da playlist dps
    path("playlist_load_modal", playlist_load_modal, name='playlist_add_view'),
    path("playlist_add_audio", playlist_add),
    path("playlist_add_play", playlist_add_play)

]
