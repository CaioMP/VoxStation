from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'channel'

urlpatterns = [
    path("myUploads", login_required(myuploads), name='myuploads'),
    path("<str:nome>/", channel, name='channel_view'),
    path("edit/<str:nome>", edit_channel, name='edit_channel_view'),
    path("playlist/<str:nome>", playlist, name='playlist_view'),
    path("about/<str:nome>", about, name='about_view'),
    path("uploads/<str:nome>", uploads, name='uploads_view'),
    path("partner/<str:nome>", partner, name='partner_view'),
    path("follow/<str:nome>", follow, name="follow_view"),
    path("playlist_all/<int:id>", playlist_all, name='playlist_all_view'),
    path("playlist_load_modal", playlist_load_modal, name='playlist_add_view'),
    path("playlist_add_audio", playlist_add),
    path("playlist_add_play", playlist_add_play),
    path('follow_general', canalSeg, name='follow_general_view'),
    path('playlist_edit', play_edit, name='play_edit_view'),
    path('vincular', vincula_play, name='vincula_view'),
    path('audio', player, name='player_view'),  # colocar o id do áudio aqui dps
    path('add_social/<str:nome>', addSocialWebs, name='add_social_view')
]
