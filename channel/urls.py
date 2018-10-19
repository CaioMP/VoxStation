from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'channel'

urlpatterns = [
    # De canal
    path("myUploads", login_required(myuploads), name='myuploads'),
    path("<int:id>/", channel, name='channel_view'),
    # path("partner/<int:id>", partner, name='partner_view'),
    path("follow/<int:id>", follow, name="follow_view"),
    path('follow_general', canalSeg, name='follow_general_view'),
    path("edit/<int:id>", edit_channel, name='edit_channel_view'),
    path('add_social/<int:id>', addSocialWebs, name='add_social_view'),
    path('chan_edit/<int:id>', channelEditInfo, name='chan_edit_info_view'),
    path('change_photo/<int:id>', changePhoto, name="change_photo_view"),
    path('change_cover/<int:id>', changeCover, name="change_cover_view"),
    path('search_audios/<int:canal_id>', search_audios, name="search_audios_view"),

    # De playlist
    path("playlist_search/<int:canal_id>", search_playlists, name='search_playlists_view'),
    path("playlist_all/<int:id>", playlist_all, name='playlist_all_view'),
    path("playlist_save/<int:playlist_id>", save_playlist, name='save_pl_view'),
    path("playlist_delete/<int:playlist_id>", delete_playlist, name='delete_pl_view'),
    path("playlist_play/<int:id>/<int:id_audio>", playlist_play, name='playlist_play_view'),
    path("playlist_load_modal", playlist_load_modal, name='playlist_add_view'),
    path("playlist_add_audio", playlist_add),
    path("playlist_add_play", playlist_add_play),
    path("playlist_del_audio/<int:playlist_id>/<int:audio_id>", del_audio_pl, name="del_audio_pl_view"),
    path('playlist_edit', play_edit, name='play_edit_view'),
    path('change_visibility_pl/<int:playlist_id>', change_visib_pl, name='change_visibility_pl'),
    path('vincular', vincula_play, name='vincula_view'),
    path('comentar/<int:audio_id>', comentar, name='comentar_view'),
    path('responder/<int:audio_id>/<int:comentario_id>', responder, name='responder_view'),
    path('randomize/<int:audio_id>/<int:playlist_id>/<int:proximo_id>', randomize, name='randomize_view'),
    path('normalize/<int:audio_id>/<int:playlist_id>/<int:proximo_id>', normalize, name='normalize_view'),
    path('random_playlist_all/<int:playlist_id>', random_playlist_all, name='random_playlist_all_view'),

    # De áudio
    path('audio/<int:id>', player, name='player_view'),
    path('ordena_audio/<int:id>', ordenaAudio, name='ordena_audio_view'),
    path('ordena_play/<int:id>', ordenaPlay, name='ordena_play_view'),
    path('change_back_audio/<int:id>', changeBackAudio, name="change_back_view"),
    path('edit_audios_capa/<int:id>/<int:id_channel>', editAudioFoto, name='edit_audio_capa_view'),
    path('edit_audios/<int:id>/<int:id_channel>', editAudio, name='edit_audio_view'),
    path('feedBack/<int:idAudio>', login_required(feedBack), name="feedBack_view"),

    path('search_tag', search_tags, name='search_tag_view')
]
