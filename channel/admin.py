from django.contrib import admin
from .models import Tag, Audio, Playlist, FeedLike, FeedDesLike


admin.site.register(Tag)
admin.site.register(Audio)
admin.site.register(Playlist)
admin.site.register(FeedLike)
admin.site.register(FeedDesLike)

