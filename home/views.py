from django.shortcuts import render
from account.models import Canal
from channel.models import Playlist
from channel.models import Audio,Anuncio
from .process import GambiNice


def IndexView(request):
    contexto = {}
    contexto['channels'] = GambiNice(Canal.objects.all())
    contexto['logado'] = request.user.is_active
    if contexto['logado']:
        contexto['playlists'] = Playlist.objects.filter(proprietario=request.user)
        contexto['canais_para_playlist'] = Canal.objects.filter(proprietario=request.user)
    return render(request, './home/index.html', contexto)


def search(request):
    return render(request, './home/search.html')
