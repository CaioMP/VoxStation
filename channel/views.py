from django.shortcuts import render, redirect, HttpResponse
from .forms import *
from account.models import Seg, MyUser
from .process import *
from django.http import JsonResponse
from .models import Playlist, Audio, Comentario, Resposta, Historico, NotificAudio, Favorito,FeedDesLike,FeedLike
from datetime import datetime
import random


def myuploads(request):
    audio = Audio()

    canais_side = Canal.objects.filter(seguidor=request.user)
    playlist_side = Playlist.objects.filter(proprietario=request.user)

    ntfs_audios = NotificAudio.objects.filter(user_notific=request.user)
    notifications = 0
    new_notific = 0

    if ntfs_audios.exists():
        for ntf in ntfs_audios.all():
            if not ntf.visualized:
                new_notific += 1
            notifications += 1

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

            # Criando a notificação para quando o áudio é enviado
            canal = Canal.objects.get(pk=audio.canal_proprietario.pk)
            if canal.users_notific:
                for user in canal.users_notific.all():
                    notification = NotificAudio()
                    notification.user_notific = user
                    notification.audio = audio
                    notification.save()

            tagtext = tagform.cleaned_data['text']
            taglist = tagprocess(tagtext)
            print(taglist)
            for tagitem in taglist:
                query = Tag.objects.filter(nome=tagitem)
                if query.exists():
                    query = Tag.objects.get(nome=tagitem)
                    print(query)
                    print('ja existia no banco a tag {}'.format(query.nome))
                    audio.tag.add(query)
                    audio.save()
                else:
                    query = Tag.objects.create(nome=tagitem)
                    query.save()
                    print(query)
                    print("foi criada a tag {} agora".format(query.nome))
                    query = Tag.objects.get(nome=tagitem)
                    print(query)
                    audio.tag.add(query)
                    audio.save()

            return redirect('/')
        else:
            has_error = True
            contexto={'form': form, 'channels': channels, 'logado': request.user.is_active, "tagform": tagform,
                      "has_error": has_error, "play_side": playlist_side, "canal_side": canais_side, 'ntfs_audios': ntfs_audios,
                      'new_notific': new_notific, 'notifications': notifications, "footer": True}

            return render(request, "./channel/myuploads.html", contexto)
    tagform = TagForm()
    form = AudioForm(instance=request.user)
    contexto = {'form': form, 'channels': channels, 'logado': request.user.is_active, 'notifications': notifications,
                "tagform": tagform, "play_side": playlist_side, "canal_side": canais_side, 'ntfs_audios': ntfs_audios,
                'new_notific': new_notific, "footer": True}

    return render(request, "./channel/myuploads.html", contexto)


def channel(request,id):
    contexto={}

    if request.user.is_active:
        contexto['play_side'] = Playlist.objects.filter(proprietario=request.user)
        contexto['canal_side'] = Canal.objects.filter(seguidor=request.user)
        ntfs_audios = NotificAudio.objects.filter(user_notific=request.user)
        notifications = 0
        new_notific = 0

        if ntfs_audios.exists():
            for ntf in ntfs_audios.all():
                if not ntf.visualized:
                    new_notific += 1
                notifications += 1

        contexto['notifications'] = notifications
        contexto['new_notific'] = new_notific
        contexto['ntfs_audios'] = ntfs_audios

    contexto['chan'] = getaudios(Canal.objects.get(pk=id))
    contexto['botao'] = ve_se_follow(request, contexto['chan'])
    contexto['cor'] = ve_se_follow(request, contexto['chan'], 1)
    contexto['num_seguidores'] = contexto['chan'].seguidor.all().count()
    contexto['logado'] = request.user.is_active
    if request.user == contexto['chan'].proprietario:
        contexto['direito_edicao']=True
    else:
        contexto['direito_edicao']=False

    return render(request, './channel/channel.html', contexto)


def playlist(request, id):
    contexto = {}

    if request.user.is_active:
        contexto['play_side'] = Playlist.objects.filter(proprietario=request.user)
        contexto['canal_side'] = Canal.objects.filter(seguidor=request.user)
        ntfs_audios = NotificAudio.objects.filter(user_notific=request.user)
        notifications = 0
        new_notific = 0

        if ntfs_audios.exists():
            for ntf in ntfs_audios.all():
                if not ntf.visualized:
                    new_notific += 1
                notifications += 1

        contexto['notifications'] = notifications
        contexto['new_notific'] = new_notific
        contexto['ntfs_audios'] = ntfs_audios

    contexto['logado'] = request.user.is_active
    contexto['chan'] = Canal.objects.get(pk=id)
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


def playlist_play(request, id, id_audio):
    comentarios = Comentario.objects.filter(audio_comentado=id_audio)
    respostas = Resposta.objects.filter(audio_comentado=id_audio)
    playlist = Playlist.objects.get(pk=id)
    audio = Audio.objects.get(pk=id_audio)
    anterior = audioposition(audio, playlist)[0]
    proximo = audioposition(audio, playlist)[1]
    n_comentarios = get_n_comentarios(comentarios, respostas)
    ordem = True  # True para aleatório

    history = Historico.objects.get(prop=request.user)
    h = Historico.objects.filter(prop=request.user, audio=audio)
    if h.exists():
        history.audio.remove(audio)
    history.audio.add(audio)
    history.save()
    comentario_form = ComentarioForm()
    resposta_form = RespostaForm(prefix="resposta")

    canal_proprietario = Canal.objects.get(nome_canal=audio.canal_proprietario)

    playlist1 = []
    playlist2 = []
    audios = []

    for audio_y in Audio.objects.all():
        audios.append(audio_y)

    random.shuffle(audios)

    for audio_x in audios:
        if len(playlist1) < 6:
            playlist1.append(audio_x)
        elif len(playlist2) < 6:
            playlist2.append(audio_x)

    if 'randomize' in request.COOKIES:
        ordem = False
        proximo.pk = random_playlist(audio, playlist, proximo.pk)
    else:
        ordem = True

    context = {
        'playlist': playlist,
        'audio': audio,
        'ordem': ordem,
        'proximo': proximo.pk,
        'anterior': anterior.pk,
        'canal_proprietario': canal_proprietario,
        'playlist1': playlist1,
        'playlist2': playlist2,
        'logado': request.user.is_active,
        'comentario_form': comentario_form,
        'resposta_form': resposta_form,
        'comentarios': comentarios,
        'respostas': respostas,
        'n_comentarios': n_comentarios
    }
    if context['canal_proprietario'].seguidor.filter(pk=request.user.id).exists():
        context['btn_message'] = 'Sintonizado'
        context['btn_color'] = 'background:#2ecc71;'
    else:
        context['btn_message'] = 'Sintonizar'
        context['btn_color'] = ''
    audio.reproducoes += 1
    audio.save()

    if request.user.is_active:
        context['play_side'] = Playlist.objects.filter(proprietario=request.user)
        context['canal_side'] = Canal.objects.filter(seguidor=request.user)
        ntfs_audios = NotificAudio.objects.filter(user_notific=request.user)
        notifications = 0
        new_notific = 0

        if ntfs_audios.exists():
            for ntf in ntfs_audios.all():
                if not ntf.visualized:
                    new_notific += 1
                notifications += 1

        context['notifications'] = notifications
        context['new_notific'] = new_notific
        context['ntfs_audios'] = ntfs_audios

    return render(request, './channel/playlist_play.html', context)


def comentar(request, audio_id):
    audio = Audio.objects.get(pk=audio_id)

    if request.method == 'POST':
        comentario_form = ComentarioForm(request.POST)
        if comentario_form.is_valid():
            comentario = Comentario()
            comentario.conteudo = request.POST['conteudo']
            comentario.comentarista = request.user
            comentario.audio_comentado = audio
            comentario.save()

    return HttpResponse("comentário salvo")


# Ordem aleatória para a playlist
def randomize(request, audio_id, playlist_id, proximo_id):
    audio = Audio.objects.get(pk=audio_id)
    playlist = Playlist.objects.get(pk=playlist_id)
    proximo_id = random_playlist(audio, playlist, proximo_id)
    ordem = "randomize"

    data = {
        'message': 'Reprodução aleatória',
        'playlist': playlist_id,
        'proximo': proximo_id
    }

    response = JsonResponse(data)
    response.set_cookie("randomize", ordem)

    return response


# Ordem normal da playlist
def normalize(request, audio_id, playlist_id, proximo_id):
    audio = Audio.objects.get(pk=audio_id)
    playlist = Playlist.objects.get(pk=playlist_id)
    proximo = audioposition(audio, playlist)[1]

    data = {
        'message': 'Reprodução aleatória',
        'playlist': playlist_id,
        'proximo': proximo.pk
    }

    response = JsonResponse(data)
    response.delete_cookie('randomize')

    return response


def responder(request, audio_id, comentario_id):
    audio = Audio.objects.get(pk=audio_id)
    comentario = Comentario.objects.get(pk=comentario_id)

    if request.method == 'POST':
        resposta_form = RespostaForm(request.POST)
        if resposta_form.is_valid():
            resposta = Resposta()
            resposta.conteudo = request.POST['conteudo']
            resposta.comentarista = request.user
            resposta.audio_comentado = audio
            resposta.comentario_em_questao = comentario
            comentario.possui_resposta += 1
            resposta.save()
            comentario.save()

    return HttpResponse("resposta salva")


def about(request, id):
    contexto = {}

    if request.user.is_active:
        contexto['play_side'] = Playlist.objects.filter(proprietario=request.user)
        contexto['canal_side'] = Canal.objects.filter(seguidor=request.user)
        ntfs_audios = NotificAudio.objects.filter(user_notific=request.user)
        notifications = 0
        new_notific = 0

        if ntfs_audios.exists():
            for ntf in ntfs_audios.all():
                if not ntf.visualized:
                    new_notific += 1
                notifications += 1

        contexto['notifications'] = notifications
        contexto['new_notific'] = new_notific
        contexto['ntfs_audios'] = ntfs_audios

    contexto['logado'] = request.user.is_active
    contexto['chan'] = Canal.objects.get(pk=id)
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


def uploads(request, id):
    contexto= {}

    if request.user.is_active:
        contexto['play_side'] = Playlist.objects.filter(proprietario=request.user)
        contexto['canal_side'] = Canal.objects.filter(seguidor=request.user)
        ntfs_audios = NotificAudio.objects.filter(user_notific=request.user)
        notifications = 0
        new_notific = 0

        if ntfs_audios.exists():
            for ntf in ntfs_audios.all():
                if not ntf.visualized:
                    new_notific += 1
                notifications += 1

        contexto['notifications'] = notifications
        contexto['new_notific'] = new_notific
        contexto['ntfs_audios'] = ntfs_audios

    contexto['logado'] = request.user.is_active
    contexto['chan'] = Canal.objects.get(pk=id)
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


def partner(request, id):
    contexto = {}

    if request.user.is_active:
        contexto['play_side'] = Playlist.objects.filter(proprietario=request.user)
        contexto['canal_side'] = Canal.objects.filter(seguidor=request.user)
        ntfs_audios = NotificAudio.objects.filter(user_notific=request.user)
        notifications = 0
        new_notific = 0

        if ntfs_audios.exists():
            for ntf in ntfs_audios.all():
                if not ntf.visualized:
                    new_notific += 1
                notifications += 1

        contexto['notifications'] = notifications
        contexto['new_notific'] = new_notific
        contexto['ntfs_audios'] = ntfs_audios

    contexto['chan'] = getaudios(Canal.objects.get(pk=id))
    contexto['botao'] = ve_se_follow(request, contexto['chan'])
    contexto['cor'] = ve_se_follow(request, contexto['chan'], 1)
    contexto['num_seguidores'] = contexto['chan'].seguidor.all().count()
    contexto['logado'] = request.user.is_active
    if request.user == contexto['chan'].proprietario:
        contexto['direito_edicao'] = True
    else:
        contexto['direito_edicao'] = False

    return render(request, './channel/similar.html', contexto)


def follow(request, id):
    json_context = {}
    canal = Canal.objects.get(pk=id)
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

    if request.user.is_active:
        contexto['play_side'] = Playlist.objects.filter(proprietario=request.user)
        contexto['canal_side'] = Canal.objects.filter(seguidor=request.user)
        contexto['channels'] = Canal.objects.filter(proprietario=request.user)
        ntfs_audios = NotificAudio.objects.filter(user_notific=request.user)
        notifications = 0
        new_notific = 0

        if ntfs_audios.exists():
            for ntf in ntfs_audios.all():
                if not ntf.visualized:
                    new_notific += 1
                notifications += 1

        contexto['notifications'] = notifications
        contexto['new_notific'] = new_notific
        contexto['ntfs_audios'] = ntfs_audios

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
    contexto['id_audio'] = contexto['playlist'].audios.first()
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
    contexto['playlist'].reproducoes += 1
    contexto['playlist'].save()
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


def edit_channel(request, id):
    contexto = {}
    if request.user.is_active:
        contexto['play_side'] = Playlist.objects.filter(proprietario=request.user)
        contexto['canal_side'] = Canal.objects.filter(seguidor=request.user)
        ntfs_audios = NotificAudio.objects.filter(user_notific=request.user)
        notifications = 0
        new_notific = 0

        if ntfs_audios.exists():
            for ntf in ntfs_audios.all():
                if not ntf.visualized:
                    new_notific += 1
                notifications += 1

        contexto['notifications'] = notifications
        contexto['new_notific'] = new_notific
        contexto['ntfs_audios'] = ntfs_audios

    contexto['audios_edit'] = EditAudioForm()
    contexto['Tag_edit'] = TagForm()
    contexto['capa_audio_form'] = EditCapaAudioForm()
    contexto['logado'] = request.user.is_active
    contexto['foto_form'] = FotoCanalForm()
    contexto['remove_form'] = RemoveAudio()
    contexto['audio_form'] = AudioDeFundoForm()
    contexto['capa_form'] = CanalCapaForm()
    contexto['chan'] = Canal.objects.get(pk=id)
    contexto['audios'] = Audio.objects.filter(canal_proprietario=contexto['chan'])
    contexto['playlists'] = ordena_pra_exibicao(Playlist.objects.filter(canal=contexto['chan']))
    if request.user == contexto['chan'].proprietario:
        contexto['num_seguidores'] = contexto['chan'].seguidor.all().count()
        if not request.user.is_active:
            redirect('/')
    else:
        redirect('/')

    if request.method == "POST":
        remove_audio = RemoveAudio(request.POST)

        if remove_audio.is_valid():
            if request.POST['remove'] == "removido":
                audio = Audio.objects.filter(titulo=request.POST['audio_removido'])  # Pega o áudio que será removido
                if audio.exists():
                    audio_removido = audio.first()
                    audio_removido.delete()

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


def player(request, id):
    comentarios = Comentario.objects.filter(audio_comentado=id)
    respostas = Resposta.objects.filter(audio_comentado=id)
    n_comentarios = get_n_comentarios(comentarios, respostas)

    comentario_form = ComentarioForm()
    resposta_form = RespostaForm(prefix="resposta")

    audio = Audio.objects.get(pk=id)
    canal_proprietario = Canal.objects.get(nome_canal=audio.canal_proprietario)

    history = Historico.objects.get(prop=request.user)
    htest = Historico.objects.filter(prop=request.user, audio=audio)
    if htest.exists():
        history.audio.remove(audio)
    history.audio.add(audio)

    history.save()

    playlist1 = []
    playlist2 = []
    audios = []

    for audio_y in Audio.objects.all():
        audios.append(audio_y)

    random.shuffle(audios)

    for audio_x in audios:
        if len(playlist1) < 6:
            playlist1.append(audio_x)
        elif len(playlist2) < 6:
            playlist2.append(audio_x)

    proximo = audios[0]

    context = {
        'audio': audio,
        'proximo': proximo.pk,
        'canal_proprietario': canal_proprietario,
        'playlist1': playlist1,
        'playlist2': playlist2,
        'logado': request.user.is_active,
        'comentario_form': comentario_form,
        'resposta_form': resposta_form,
        'comentarios': comentarios,
        'respostas': respostas,
        'n_comentarios': n_comentarios
    }
    if context['canal_proprietario'].seguidor.filter(pk=request.user.id).exists():
        context['btn_message'] = 'Sintonizado'
        context['btn_color'] = 'background:#2ecc71;'
    else:
        context['btn_message'] = 'Sintonizar'
        context['btn_color'] = ''

    audio.reproducoes += 1
    audio.save()

    if request.user.is_active:
        context['play_side'] = Playlist.objects.filter(proprietario=request.user)
        context['canal_side'] = Canal.objects.filter(seguidor=request.user)
        ntfs_audios = NotificAudio.objects.filter(user_notific=request.user)
        notifications = 0
        new_notific = 0

        if ntfs_audios.exists():
            for ntf in ntfs_audios.all():
                if not ntf.visualized:
                    new_notific += 1
                notifications += 1

        context['notifications'] = notifications
        context['new_notific'] = new_notific
        context['ntfs_audios'] = ntfs_audios

    return render(request, './channel/player.html', context)


def addSocialWebs(request, id):
    redes = {}
    json_context = {}
    canal_detentor = id
    redes['facebook'] = request.GET['facebook']
    redes['instagram'] = request.GET['instagram']
    redes['twitter'] = request.GET['twitter']
    redes['youtube'] = request.GET['youtube']
    redes['twitch'] = request.GET['twitch']
    redes['googleplus'] = request.GET['googleplus']
    validacao = validaSocialWebs(redes, canal_detentor)
    certificado_links = certifica_link(redes)
    if validacao['status']:
        canal = Canal.objects.get(pk=id)
        canal.facebook = redes['facebook']
        canal.instagram = redes['instagram']
        canal.twitch = redes['twitch']
        canal.twitter = redes['twitter']
        canal.youtube = redes['youtube']
        canal.googleplus = redes['googleplus']
        canal.save()

    return JsonResponse(validacao)


def ordenaAudio(request,id):
    json = {}
    op = request.GET['opcao']
    canal = Canal.objects.get(nome_canal=id)

    if op == 'recentes':
        audios = Audio.objects.filter(canal_proprietario=canal).order_by('data_publicacao').reverse()
    elif op == 'antigos':
        audios = Audio.objects.filter(canal_proprietario=canal).order_by('data_publicacao')
    elif op == 'populares':
        audios = Audio.objects.filter(canal_proprietario=canal).order_by('reproducoes')
    json['html'] = setOrdemAudios(audios)
    return JsonResponse(json)


def ordenaPlay(request, id):
    json_context = {}
    canal = Canal.objects.get(pk=id)
    op = request.GET['opcao']
    if op == "recentes":
        playlists = Playlist.objects.filter(canal=canal).order_by('ultima_atualizacao').reverse()
    elif op == 'antigos':
        playlists = Playlist.objects.filter(canal=canal).order_by('ultima_atualizacao')
    elif op == "mais audios":
        playlists = Playlist.objects.filter(canal=canal).order_by('numero_de_audios').reverse()
    elif op == "menos audios":
        playlists = Playlist.objects.filter(canal=canal).order_by('numero_de_audios')
    json_context['html'] = setOrdemPlaylists(playlists)
    return JsonResponse(json_context)


def channelEditInfo(request, id):
    canal = Canal.objects.get(pk=id)
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


def changeCover(request, id):
    chan = Canal.objects.get(pk=id)

    if request.method == "POST":
        Capa = CanalCapaForm(request.POST, request.FILES, instance=request.user)
        print('oi')
        print(Capa.is_valid())
        if Capa.is_valid():
            Capa.save(commit=False)
            chan.capa.delete(save=True)
            print('foi')
            chan.capa = Capa.cleaned_data['capa']
            chan.save()
    return redirect('/channel/edit/{}'.format(id))


def changeBackAudio(request,id):
    chan = Canal.objects.get(pk=id)

    if request.method == "POST":
        audio = AudioDeFundoForm(request.POST, request.FILES, instance=request.user)
        if audio.is_valid():
            audio.save(commit=False)
            chan.audio_fundo.delete(save=True)
            chan.audio_fundo = audio.cleaned_data['audio_fundo']
            chan.save()
    return redirect('/channel/edit/{}'.format(id))


def changePhoto(request, id):
    chan = Canal.objects.get(pk=id)

    if request.method == 'POST':
        photo = FotoCanalForm(request.POST, request.FILES, instance=request.user)
        print("chegou")
        print(photo.is_valid())
        if photo.is_valid():
            photo.save(commit=False)
            chan.foto_canal.delete(save=True)
            chan.foto_canal = photo.cleaned_data['foto_canal']
            print('trocou')
            chan.save()
    return redirect('/channel/edit/{}'.format(id))


def editAudioFoto(request, id, id_channel):
    if request.method == "POST":
       capaform = capaForm(request.POST, request.FILES)
       if capaform.is_valid():
            capaform.save(commit=False)
            audio = Audio.objects.get(pk=id)
            audio.capa.delete(save=True)
            audio.capa = capaform.cleaned_data['capa']
            audio.save()
    return redirect("/channel/edit/{}".format(id_channel))


def editAudio(request, id, id_channel):
    if request.method == "POST":
        tag = TagForm(request.POST, request.FILES)
        audio_form = EditAudioForm(request.POST)
        print(tag.is_valid())
        print(audio_form.is_valid())
        if tag.is_valid() and audio_form.is_valid():
            print('ta valido')
            audio = Audio.objects.get(pk=id)
            audio.titulo = audio_form.cleaned_data['titulo']
            audio.descricao = audio_form.cleaned_data['descricao']
            tags = tagprocess(tag.cleaned_data['text'])
            audio.tag.clear()
            for tag in tags:
                query = Tag.objects.filter(nome=tag)
                if query.exists():
                    query = Tag.objects.get(nome=tag)
                    print(query)
                    print('ja existia no banco a tag {}'.format(query.nome))
                    audio.tag.add(query)
                    audio.save()
                else:
                    query = Tag.objects.create(nome=tag)
                    query.save()
                    query = Tag.objects.get(nome=tag)
                    audio.tag.add(query)
                    audio.save()
    return redirect("/channel/edit/{}".format(id_channel))

def feedBack(request, idAudio):
    json_context = {}
    audio = Audio.objects.get(pk=idAudio)
    opcao = request.GET['opcao']
    conta = MyUser.objects.get(pk=request.user.pk)
    Fav = Favorito.objects.get(prop=request.user)

    if opcao == "like":
        if FeedLike.objects.filter(conta_feed=request.user.pk, Audio_feed=audio).exists():
            feed = FeedLike.objects.get(conta_feed=request.user.pk, Audio_feed=audio).delete()
            audio.numero_likes -= 1
            json_context['message'] = "audio removido dos favoritos"
        else:
            feed = FeedLike.objects.create(conta_feed=request.user.pk, Audio_feed=audio)
            audio.numero_likes += 1
            audio.save()
            Fav.audio.add(audio)
            Fav.save()
            json_context['message'] = "audio adicionado aos favoritos"
            if FeedDesLike.objects.filter(conta_feed=request.user.pk, Audio_feed=audio).exists():
                feed = FeedLike.objects.get(conta_feed=request.user.pk, Audio_feed=audio).delete()

                audio.numero_deslikes -= 1

    else:
        if FeedDesLike.objects.filter(conta_feed=request.user.pk, Audio_feed=audio).exists():
            feed = FeedLike.objects.get(conta_feed=request.user.pk, Audio_feed=audio).delete()

            audio.numero_deslikes -= 1

        else:
            feed = FeedLike.objects.create(conta_feed=request.user.pk, Audio_feed=audio)

            audio.numero_deslikes += 1
            json_context['message'] = "audio removido dos favoritos"
            Fav.audio.remove(audio)
            Fav.save()

            if FeedLike.objects.filter(conta_feed=request.user.pk, Audio_feed=audio).exists():
                feed = FeedLike.objects.get(conta_feed=request.user.pk, Audio_feed=audio).delete()

                audio.numero_likes -= 1
    feed.save()
    audio.save()

    json_context['numero_likes'] = audio.numero_likes
    json_context['numero_deslikes'] = audio.numero_deslikes

    return JsonResponse(json_context)





