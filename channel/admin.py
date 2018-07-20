from django.contrib import admin
from .models import Tag, Audio, Playlist, FeedLike, FeedDesLike, CanalPlay


admin.site.register(Tag)
admin.site.register(Audio)
admin.site.register(Playlist)
admin.site.register(FeedLike)
admin.site.register(FeedDesLike)
admin.site.register(CanalPlay)
