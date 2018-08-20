from django.shortcuts import render
from account.models import Canal
from channel.models import Playlist
from channel.models import Audio, Anuncio
from .process import *
from channel.process import ordena_pra_exibicao

def IndexView(request):
    contexto = {}
    contexto['channels'] = GambiNice(Canal.objects.all())
    contexto['logado'] = request.user.is_active
    if contexto['logado']:
        contexto['playlists'] = Playlist.objects.filter(proprietario=request.user)
        contexto['canais_para_playlist'] = Canal.objects.filter(proprietario=request.user)
    return render(request, './home/index.html', contexto)


def search(request):
    contexto = {}
    if request.method == "POST":
        pesquisa = request.POST['pesquisa']
        contexto['pesquisa'] = pesquisa
        contexto['canais'] = Canal.objects.filter(nome_canal__contains=pesquisa)
        contexto['audios'] = Audio.objects.filter(titulo__contains=pesquisa)
        contexto['playlists_show'] = Playlist.objects.filter(nome__contains=pesquisa)
        contexto['canais'] = checkExist(contexto['canais'])
        contexto['audios'] = checkExist(contexto['audios'])
        if contexto['canais'] != False:
            contexto['canais'] = contaSeg(contexto['canais'])
        contexto['playlists_show'] = checkExist(contexto['playlists_show'])
        if contexto['playlists_show'] != False:
            contexto['playlists_show'] = ordena_pra_exibicao(contexto['playlists_show'])
        contexto['tot_result'], contexto['tot_playlists'], contexto['tot_audios'], contexto['tot_canais'] = contaResultados(contexto['canais'], contexto['audios'], contexto['playlists_show'])

    return render(request, './home/search.html', contexto)

