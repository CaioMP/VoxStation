from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'channel'

urlpatterns = [
    path("myUploads", login_required(myuploads), name='myuploads'),
    path("<int:id>/", channel, name='channel_view'),
    path("edit/<int:id>", edit_channel, name='edit_channel_view'),
    path("playlist/<int:id>", playlist, name='playlist_view'),
    path("about/<int:id>", about, name='about_view'),
    path("uploads/<int:id>", uploads, name='uploads_view'),
    path("partner/<int:id>", partner, name='partner_view'),
    path("follow/<int:id>", follow, name="follow_view"),
    path("playlist_all/<int:id>", playlist_all, name='playlist_all_view'),
    path("playlist_load_modal", playlist_load_modal, name='playlist_add_view'),
    path("playlist_add_audio", playlist_add),
    path("playlist_add_play", playlist_add_play),
    path('follow_general', canalSeg, name='follow_general_view'),
    path('playlist_edit', play_edit, name='play_edit_view'),
    path('vincular', vincula_play, name='vincula_view'),
    path('audio', player, name='player_view'),  # colocar o id do áudio aqui dps
    path('add_social/<int:id>', addSocialWebs, name='add_social_view'),
    path('ordena_audio/<int:id>', ordenaAudio, name='ordena_audio_view'),
    path('ordena_play/<int:id>', ordenaPlay, name='ordena_play_view'),
    path('chan_edit/<int:id>', channelEditInfo,name='chan_edit_info_view')
]
