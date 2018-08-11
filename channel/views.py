from django.shortcuts import render, redirect, HttpResponse
from .forms import AudioForm, TagForm, SearchChannelAudioForm,PlaylistForm,capaForm
from account.models import Canal, Seg
from .process import *
from django.http import JsonResponse
from .models import Playlist, Audio
from datetime import datetime
from django.db.models import Sum


def myuploads(request):
    audio = Audio()
    channels = Canal.objects.filter(proprietario=request.user)

    if request.method == "POST":
        tagform = TagForm(request.POST, request.FILES)
        form = AudioForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid() and tagform.is_valid():
            form.save(commit=False)
            audio.canal_proprietario = form.cleaned_data["canal_proprietario"]
            audio.titulo = form.cleaned_data['titulo']
            audio.audio = form.cleaned_data['audio']
            audio.descricao = form.cleaned_data['descricao']
            audio.capa = form.cleaned_data['capa']
            audio.reproducoes = 0
            audio.proprietario = request.user
            audio.save()
            tagtext = tagform.cleaned_data['text']
            taglist = tagprocess(tagtext)
            for tagitem in taglist:
                query = Tag.objects.filter(nome=tagitem)
                if query.exists():
                    audio.tag.set(query)
                    audio.save()
                else:
                    query = Tag.objects.create(nome=tagitem)
                    query.save()
                    query = Tag.objects.filter(nome=tagitem)
                    audio.tag.set(query)
                    audio.save()

            return redirect('/')
        else:
            erro = True
            return render(request, "./channel/myuploads.html", {'form': form, 'channels': channels, 'logado': request.user.is_active,
                                                                "tagform": tagform, "erro": erro})
    tagform = TagForm()
    form = AudioForm(instance=request.user)
    return render(request, "./channel/myuploads.html", {'form': form, 'channels': channels,
                                                        "tagform": tagform, 'logado': request.user.is_active})


def channel(request, nome):
    contexto={}
    contexto['chan'] = getaudios(Canal.objects.get(nome_canal=nome))
    contexto['botao'] = ve_se_follow(request, contexto['chan'])
    contexto['cor'] = ve_se_follow(request, contexto['chan'], 1)
    contexto['num_seguidores'] = contexto['chan'].seguidor.all().count()
    contexto['logado'] = request.user.is_active
    if request.user == contexto['chan'].proprietario:
        contexto['direito_edicao']=True
    else:
        contexto['direito_edicao']=False
    return render(request, './channel/channel.html', contexto)


def playlist(request, nome):
    contexto = {}
    contexto['logado'] = request.user.is_active
    contexto['chan'] = Canal.objects.get(nome_canal=nome)
    contexto['playlists'] = Playlist.objects.filter(canal=contexto['chan'])
    contexto['playlists'] = ordena_pra_exibicao(contexto['playlists'])
    contexto['botao'] = ve_se_follow(request, contexto['chan'])
    contexto['cor'] = ve_se_follow(request, contexto['chan'], 1)
    if request.user == contexto['chan'].proprietario:
        contexto['direito_edicao'] = True
    else:
        contexto['direito_edicao'] = False
    contexto['num_seguidores'] = contexto['chan'].seguidor.all().count()
    return render(request, './channel/playlists.html', contexto)


def about(request, nome):
    contexto = {}
    contexto['logado'] = request.user.is_active
    contexto['chan'] = Canal.objects.get(nome_canal=nome)
    contexto['botao'] = ve_se_follow(request, contexto['chan'])
    contexto['cor'] = ve_se_follow(request, contexto['chan'], 1)
    contexto['num_seguidores'] = contexto['chan'].seguidor.all().count()
    audios = Audio.objects.filter(canal_proprietario=contexto['chan'])
    contexto['likes'] = get_status_channel(audios, 'likes')
    contexto['deslikes'] = get_status_channel(audios, 'deslikes')
    contexto['reproducoes_tot'] = get_status_channel(audios)
    contexto['tags_mais_usadas'] = get_tags(audios)
    if request.user == contexto['chan'].proprietario:
        contexto['direito_edicao'] = True
    else:
        contexto['direito_edicao'] = False
    return render(request, './channel/about.html', contexto)


def uploads(request, nome):
    contexto= {}
    contexto['logado'] = request.user.is_active
    contexto['chan'] = Canal.objects.get(nome_canal=nome)
    contexto['botao'] = ve_se_follow(request, contexto['chan'])
    contexto['cor'] = ve_se_follow(request, contexto['chan'], 1)
    contexto['num_seguidores'] = contexto['chan'].seguidor.all().count()
    if request.user == contexto['chan'].proprietario:
        contexto['direito_edicao'] = True
    else:
        contexto['direito_edicao'] = False

    if request.method == 'POST':
        search_form = SearchChannelAudioForm(request.POST)

        if search_form.is_valid():
            search = search_form.cleaned_data['text']
            audios = searchclear(search, contexto['chan'])
            contexto['audios'] = audios
            contexto['form_aud'] = SearchChannelAudioForm()
            return render(request, './channel/uploads.html', contexto)
        else:
            contexto['erro'] = True
            contexto['form_aud'] = SearchChannelAudioForm()
            return render(request, './channel/uploads.html', contexto)
    else:
        audios = Audio.objects.filter(canal_proprietario=contexto['chan']).order_by('data_publicacao').reverse()
        contexto['audios'] = audios
        contexto['form_aud'] = SearchChannelAudioForm()
        return render(request, './channel/uploads.html', contexto)


def partner(request, nome):
    return render(request, './channel/similar.html')


def follow(request, nome):
    json_context = {}
    canal = Canal.objects.get(nome_canal=nome)
    seguidor = canal.seguidor.filter(pk=request.user.pk)
    if seguidor.exists():
        Seg.objects.get(canal_seguido=canal, seguidores=request.user).delete()
        json_context['estado'] = "sintonizar"
        json_context['cor'] = "#00000085"

    else:
        Seg.objects.create(canal_seguido=canal, seguidores=request.user, estado=0)
        json_context['estado'] = "sintonizado"
        json_context['cor'] = "#2ecc71"
    json_context['num_seg'] = str(canal.seguidor.all().count())+" seguidores"
    return JsonResponse(json_context)


def playlist_all(request, id):
    contexto = {}
    contexto['channels'] = Canal.objects.filter(proprietario=request.user)
    contexto['form'] = PlaylistForm()
    contexto['capa_form'] = capaForm()
    play = Playlist.objects.get(pk=id)
    if request.method == 'POST':
        contexto['dados_retornados'] = PlaylistForm(request.POST, instance=request.user)
        contexto['capa_retornada'] = capaForm(request.POST, request.FILES, instance=request.user)
        if contexto['capa_retornada'].is_valid():
            contexto['capa_retornada'].save(commit=False)
            play.capa.delete(save=True)
            play.capa = contexto['capa_retornada'].cleaned_data['capa']
            play.save()
    contexto['playlist'] = Playlist.objects.get(pk=id)
    if contexto['playlist'].proprietario == request.user:
        contexto['direito_edicao'] = True
    else:
        contexto['direito_edicao'] = False
    if contexto['playlist'].canal:
        contexto['canal'] = contexto['playlist'].canal
        if contexto['canal'].seguidor.filter(pk=request.user.id).exists():
            contexto['btn_message'] = 'Sintonizado'
            contexto['btn_color'] = 'background:#2ecc71;'
        else:
            contexto['btn_message'] = 'Sintonizar'
            contexto['btn_color'] = ''

    if contexto['playlist'].descricao == '':
        contexto['tem_desc'] = False
    else:
        contexto['tem_desc'] = True
    print(contexto['direito_edicao'])
    contexto['audios'] = contexto['playlist'].audios.filter()
    contexto['capa_reserva'] = contexto['playlist'].audios.order_by('reproducoes').first()
    contexto['tem_capa'] = True
    contexto['reproducoes_tot'] = contexto['playlist'].audios.filter().aggregate(Sum('reproducoes'))['reproducoes__sum']
    contexto['logado'] = request.user.is_active
    return render(request, './channel/playlist_all.html', contexto)


def playlist_load_modal(request):
    json_context = {}

    audio_cod = request.GET['aud']
    audio_set = Audio.objects.get(pk=audio_cod)
    load_modal = request.GET['load']

    json_context['html'] = gera_html(request, audio_cod)
    json_context['message'] = 'modal carregado'
    return JsonResponse(json_context)


def playlist_add(request):

    audio_cod = request.GET['aud']
    playlist = request.GET['playlist_cod']
    audio_set = Audio.objects.get(pk=audio_cod)
    play = Playlist.objects.get(pk=playlist)
    Playlist.objects.filter(pk=playlist).update(ultima_atualizacao=datetime.now())

    if play.audios.filter(pk=audio_cod).exists():
        play.audios.remove(audio_set)
        play.numero_de_audios -= 1
        play.save()
        json_context = {'message': 'Removido de '+play.nome+''}
    else:
        play.numero_de_audios += 1
        play.audios.add(audio_set)
        play.save()
        json_context = {'message': 'Adicionado a ' + play.nome + ''}
    return JsonResponse(json_context)


def playlist_add_play(request):
    json_context = {}
    play = {}
    audio_cod = request.GET['aud']
    play['nome'] = request.GET['nome']
    play['visibilidade'] = request.GET['visibilidade']
    play['canal_atrelado'] = request.GET['canal_atrelado']
    audio_set = Audio.objects.get(pk=audio_cod)
    play['criada'] = Playlist.objects.create(nome=play['nome'], visibilidade=play['visibilidade'], proprietario=request.user, capa=audio_set.capa, descricao="")
    play['criada'].audios.add(audio_set)
    play['criada'].save()
    if play['canal_atrelado'] == 'Nenhum':
        json_context['html'] = gera_html(request, audio_cod)
        json_context['message'] = 'Áudio adicionado a '+play['criada'].nome
        return JsonResponse(json_context)
    else:
        play['canal_set'] = Canal.objects.get(nome_canal=play['canal_atrelado'])
        play['criada'].canal = play['canal_set']
        play['criada'].save()
        print(play['criada'].canal)
        json_context['message'] = 'Áudio adicionado a ' + play['criada'].nome
        json_context['html'] = gera_html(request, audio_cod)
        return JsonResponse(json_context)



def edit_channel(request, nome):
    contexto = {}
    contexto['chan'] = Canal.objects.get(nome_canal=nome)
    contexto['audios'] = Audio.objects.filter(canal_proprietario=contexto['chan'])
    contexto['playlists'] = ordena_pra_exibicao(Playlist.objects.filter(canal=contexto['chan']))
    if request.user == contexto['chan'].proprietario:
        contexto['num_seguidores'] = contexto['chan'].seguidor.all().count()
        if not request.user.is_active:
            redirect('/')
    else:
        redirect('/')
    return render(request, "./channel/edit_channel.html", contexto)


def canalSeg(request):
    canal_id = request.GET['canal']
    json_context = {}
    canal = Canal.objects.get(pk=canal_id)
    if Seg.objects.filter(canal_seguido=canal, seguidores=request.user).exists():
        Seg.objects.get(canal_seguido=canal, seguidores=request.user).delete()
        json_context['message'] = 'Sintonizar'
        json_context['fundo'] = ''
    else:
        Seg.objects.create(canal_seguido=canal, seguidores=request.user)
        json_context['message'] = 'Sintonizado'
        json_context['fundo'] = 'background:#2ecc71;'

    return JsonResponse(json_context)


def play_edit(request):
    json_context = {}
    playnome = request.GET['nome']
    playDesc = request.GET['descricao']
    play_id = request.GET['id']

    play = Playlist.objects.get(pk=play_id)
    play.nome = playnome
    play.descricao = playDesc
    play.save()
    json_context['message'] = "ok"
    return JsonResponse(json_context)


def vincula_play(request):
    json_context = {}
    playlist_id = request.GET['playlist']
    canal_id = request.GET['canal']
    play = Playlist.objects.get(pk=playlist_id)
    if canal_id == '0nenhum':
        play.canal = None
        json_context['message'] = 'playlist desvinculada'
    else:
        canal_set = Canal.objects.get(nome_canal=canal_id)
        play.canal = canal_set
        json_context['message'] = 'Playlist vinculada a '+canal_set.nome_canal
    play.save()
    return JsonResponse(json_context)


def player(request):
    comentarios = [1, 2]

    return render(request, './channel/player.html', {'logado': request.user.is_active, 'comentarios': comentarios})


def addSocialWebs(request, nome):
    redes = {}
    json_context = {}
    canal_detentor = nome
    redes['facebook'] = request.GET['facebook']
    redes['instagram'] = request.GET['instagram']
    redes['twitter'] = request.GET['twitter']
    redes['youtube'] = request.GET['youtube']
    redes['twitch'] = request.GET['twitch']
    redes['googleplus'] = request.GET['googleplus']
    validacao = validaSocialWebs(redes, canal_detentor)
    certificado_links = certifica_link(redes)
    if validacao['status']:
        canal = Canal.objects.get(nome_canal=nome)
        canal.facebook = redes['facebook']
        canal.instagram = redes['instagram']
        canal.twitch = redes['twitch']
        canal.twitter = redes['twitter']
        canal.youtube = redes['youtube']
        canal.googleplus = redes['googleplus']
        canal.save()

    return JsonResponse(validacao)


def ordenaAudio(request,nome):
    json = {}
    op = request.GET['opcao']
    json['html'] = setOrdemAudios(op, nome)
    return JsonResponse(json)


def ordenaPlay(request, nome):
    json_context = {}
    canal = Canal.objects.get(nome_canal=nome)
    op = request.GET['opcao']
    json_context['html'] = setOrdemPlaylists(op, canal)
    return JsonResponse(json_context)

def channelEditInfo(request, nome):
    canal = Canal.objects.get(nome_canal=nome)
    json_context = {}
    canal_nome_novo = request.GET['nome']
    canal_descricao = request.GET['descricao']

    canal.descricao = canal_descricao
    json_context['descricao'] = canal_descricao
    if Canal.objects.filter(nome_canal=canal_nome_novo).exists() and canal.nome_canal != canal_nome_novo:
        json_context['nome'] = canal.nome_canal
        json_context['message'] = "já existe um canal com esse, nome tente outro"
    else:
        canal.nome_canal = canal_nome_novo
        json_context['nome'] = canal.nome_canal
        json_context['message'] = "atualização efetuada com sucesso"
    canal.save()
    return JsonResponse(json_context)
