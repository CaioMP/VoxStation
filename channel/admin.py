from django.contrib import admin
from .models import Tag, Audio, Playlist, FeedLike, FeedDesLike, AudioReport


class AudioAdmin(admin.ModelAdmin):
    list_display = ("titulo", "canal_proprietario")
    search_fields = ['titulo']


class AudioReportAdmin(admin.ModelAdmin):
    list_display = ("audio", "canal", "usuario")


admin.site.register(Tag)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Playlist)
admin.site.register(FeedLike)
admin.site.register(FeedDesLike)
admin.site.register(AudioReport, AudioReportAdmin)

