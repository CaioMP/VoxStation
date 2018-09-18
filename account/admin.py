from django.contrib import admin
from django.contrib.auth.models import Group

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm
from .models import MyUser, Anuncio, Seg, Canal, NotificAudio
from channel.models import Comentario, Resposta


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    list_display = ('username', 'email', 'is_admin')
    list_filter  = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'img_perfil', 'username', 'email', 'password', 'phone',
                           'genero', 'pais', 'sobre'
                           )}),
        ('Permissions', {'fields': ('is_admin',)})
    )

    search_fields = ('username', 'email')
    ordering = ('username', 'email')

    filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)
admin.site.register(Canal)
admin.site.register(NotificAudio)
admin.site.register(Comentario)
admin.site.register(Seg)
admin.site.register(Anuncio)
admin.site.register(Resposta)
admin.site.unregister(Group)
