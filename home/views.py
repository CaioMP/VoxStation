from django.shortcuts import render
from account.models import Canal
from channel.models import Playlist
from channel.models import Audio, Anuncio
from .process import *
from channel.process import ordena_pra_exibicao
from django.http import JsonResponse
from datetime import datetime



def IndexView(request):
    contexto = {}
    contexto['play_side'] = Playlist.objects.filter(proprietario=request.user)
    contexto['canal_side'] = Canal.objects.filter(seguidor=request.user)
    contexto['channels'] = orderAudios(Canal.objects.all())
    contexto['logado'] = request.user.is_active
    if contexto['logado']:
        contexto['playlists'] = Playlist.objects.filter(proprietario=request.user)
        contexto['canais_para_playlist'] = Canal.objects.filter(proprietario=request.user)

    return render(request, './home/index.html', contexto)


def search(request):
    contexto = {}
    contexto['play_side'] = Playlist.objects.filter(proprietario=request.user)
    contexto['canal_side'] = Canal.objects.filter(seguidor=request.user)
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


def playordena(request, pesquisa):
    json = {}
    op = request.GET['op']

    if op == "recentes":
        playlists = Playlist.objects.filter(nome__contains=pesquisa).order_by('ultima_atualizacao').reverse()
    elif op == 'antigos':
        playlists = Playlist.objects.filter(nome__contains=pesquisa).order_by('ultima_atualizacao')
    elif op == "mais audios":
        playlists = Playlist.objects.filter(nome__contains=pesquisa).order_by('numero_de_audios').reverse()
    json['html'] = setOrdemPlaylistsSearch(playlists)

    return JsonResponse(json)


def audioordena(request, pesquisa):
    json = {}
    op = request.GET['op']
    audios = []
    hoje = datetime.today()
    if op == 'populares':
        audios = Audio.objects.filter(titulo__contains=pesquisa).order_by('reproducoes')
    elif op == 'melhor avaliados':
        audios = Audio.objects.filter(titulo__contains=pesquisa).order_by('numero_likes')
    elif op == "recentes":
        audios = Audio.objects.filter(titulo__contains=pesquisa).order_by('data_publicacao').reverse()
    elif op == "antigos":
        audios = Audio.objects.filter(titulo__contains=pesquisa).order_by('data_publicacao')

    json['html'] = setOrdemAudiosSearch(audios)
    return JsonResponse(json)


def ordenaCanais(request, pesquisa):
    json = {}
    op = request.GET['op']

    if op == 'mais seguidores':
        canais = Canal.objects.filter(nome_canal__contains=pesquisa).order_by('numero_seguidores').reverse()
    if op == 'mais recentes':
        canais = Canal.objects.filter(nome_canal__contains=pesquisa).order_by('data_criacao').reverse()
    if op == 'mais antigos':
        canais = Canal.objects.filter(nome_canal__contains=pesquisa).order_by('data_criacao')
    json['html'] = setOrdemCanais(canais)

    return JsonResponse(json)






