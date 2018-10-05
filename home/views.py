from django.shortcuts import render, HttpResponse
from channel.models import *
from .process import *
from channel.process import ordena_pra_exibicao
from django.http import JsonResponse
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def IndexView(request):
    contexto = {}

    if request.user.is_active:
        contexto['play_side'] = Playlist.objects.filter(proprietario=request.user).order_by('-ultima_atualizacao')
        contexto['canal_side'] = Canal.objects.filter(seguidor=request.user).order_by('nome_canal')
        ntfs_audios = NotificAudio.objects.filter(user_notific=request.user).order_by('-audio')
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
        fav = FeedLike.objects.filter(conta_feed=request.user).order_by('-data_do_feed')
        contexto['audios_favoritos'] = fav.all()

    contexto['channels'] = orderAudios(Canal.objects.all())
    contexto['logado'] = request.user.is_active
    if contexto['logado']:
        contexto['playlists'] = Playlist.objects.filter(proprietario=request.user)
        contexto['canais_para_playlist'] = Canal.objects.filter(proprietario=request.user)

    return render(request, './home/index.html', contexto)


def search(request):
    contexto = {}

    if request.user.is_active:
        contexto['play_side'] = Playlist.objects.filter(proprietario=request.user).order_by('-ultima_atualizacao')
        contexto['canal_side'] = Canal.objects.filter(seguidor=request.user).order_by('nome_canal')
        ntfs_audios = NotificAudio.objects.filter(user_notific=request.user).order_by('-audio')
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

    contexto['logado'] = request.user.is_active
    return render(request, './home/search.html', contexto)


def visualized(request):
    notifications = NotificAudio.objects.filter(user_notific=request.user)
    for notific in notifications:
        if not notific.visualized:
            notific.visualized = True
            notific.save()
    return HttpResponse("visualizado")


def report_audio(request, audio_id):
    audio = Audio.objects.get(pk=audio_id)

    fromaddr = "clientvxs@gmail.com"
    toaddr = "stationvox@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Denúncia " + audio.titulo

    body = "Áudio denunciado: http://127.0.0.1:8000/channel/audio/" + str(audio.pk) + \
           "\nCanal proprietário: " + audio.canal_proprietario.nome_canal + \
           "\nUsuário proprietário: " + audio.canal_proprietario.proprietario.email + \
           "\nDenunciante: " + request.user.email + \
           "\n\nMotivo: " + request.POST['motivo'] + \
           "\nDescrição: " + request.POST['denuncia']
    msg.attach(MIMEText(body, 'plain'))

    denuncia = AudioReport()
    denuncia.motivo = request.POST['motivo']
    denuncia.descricao = request.POST['denuncia']
    denuncia.usuario = request.user
    denuncia.audio = audio
    denuncia.canal = audio.canal_proprietario
    denuncia.save()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "80251997Client@")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    return HttpResponse("Email enviado")


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







