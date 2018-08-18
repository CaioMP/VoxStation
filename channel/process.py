from .models import Tag
from .models import Audio, Playlist, Canal
from urllib import request
from datetime import datetime
def tagprocess(tagtext):
    tagl = tagtext.replace(" ", "")
    taglist = tagl.split("#")
    taglist.remove('')
    TagR = []
    for tagitem in taglist:
        TagR.append(tagitem)
    return TagR


def getaudios(canal):

    canal.playlist1 = Audio.objects.filter(canal_proprietario=canal).order_by('data_publicacao')[:4]
    canal.playlist2 = Audio.objects.filter(canal_proprietario=canal).order_by('data_publicacao')[4:8]

    return canal


def searchclear(search, canal):

    audio = Audio.objects.filter(titulo__contains=search, canal_proprietario=canal)
    if audio.exists():
        return audio
    else:
        return False


def get_status_channel(audios, op='reproducoes'):
    tot = 0
    if op == 'likes':
        for audio in audios:
            tot += audio.likes.all().count()
        return tot
    elif op == 'deslikes':
        for audio in audios:
            tot += audio.deslikes.all().count()
        return tot
    else:
        for audio in audios:
            tot += audio.reproducoes
        return tot


def get_tags(audios):
    lista_tags = []
    lista_aparicoes = []
    lista_final = []

    # resgata todos as tags de todos os audios e salva na 'lista_tags'
    for audio in audios:
        for tag in audio.tag.all():
            lista_tags.append(tag)

    # conta quantas vezes uma tag aparece na lista de tags e salva na lista de aparicoes
    for tag in lista_tags:
        lista_aparicoes.append(lista_tags.count(tag))

    # organiza a lista de aparicoes em ordem decescente
    lista_aparicoes = sorted(lista_aparicoes, reverse=True)
    # splita a lista de aparicoes nos 4 primeiros membros
    lista_aparicoes = lista_aparicoes[:4]

    # verifica se a lista o numero de vezes que um determinado elemento aparece na lista de tags e compara o numero com a lista
    # - e ve se esse numero aparece na lista de aparicoes, se sim ele salva na lista final
    for tag in lista_tags:
        if lista_tags.count(tag) in lista_aparicoes:
            lista_final.append(tag.nome)
        else:
            continue
    # retorna lista final
    return lista_final[:4]


def ve_se_follow(request,canal,op=0):

    seguidor_em_questao = canal.seguidor.filter(pk=request.user.pk)

    if op==0:
        if seguidor_em_questao.exists():
            return 'sintonizado'
        else:
            return 'sintonizar'
    else:
        if seguidor_em_questao.exists():
            return '#2ecc71'
        else:
            return '#00000085'


def gera_html(request, audio):
    plays = Playlist.objects.filter(proprietario=request.user)
    html = ""

    for play in plays:
        if play.audios.filter(pk=audio).exists():
            html += '<label class="pl-label ">'+play.nome+'<input type="checkbox" aud="1" class="play_id" checked="checked" url_="channel/playlist_add" id="'+str(play.id)+'" > <span class="checkmark"></span></label><a href="#"><i class="fas fa-trash-alt fas-playlist"></i></a><br><br><br>'
        else:
            html += '<label class="pl-label ">' + play.nome + '<input type="checkbox" aud="1" class="play_id" url_="channel/playlist_add" id="'+str(play.id)+'" ><span class="checkmark addplay_id" value="'+str(play.id)+'" url_="channel/playlist_add" ></span></label><a href="#"><i class="fas fa-trash-alt fas-playlist"></i></a><br><br><br>'

    return html


def ordena_pra_exibicao(playlists):

    for playlist in playlists:
        playlist.audios_apresentaveis = playlist.audios.filter().order_by('reproducoes')[:4]
    return playlists


def validaSocialWebs(redes, canal_id):
    errosInvalido = []
    errosNotFound = []
    erros_de_pagina = []
    mensagem = {}
    alterados = []
    canal = Canal.objects.get(pk=canal_id)
    for rede in redes:
        if redes[rede].isspace() or redes[rede] == '':
            continue
        else:
            try:
                a = request.urlopen(redes[rede])
            except ValueError:
                errosInvalido.append(rede)
            except request.HTTPError as e:
                print(e.getcode())
                errosNotFound.append(rede)
            else:
                continue
    if len(errosInvalido) != 0:
        mensagem['status'] = False
        mensagem['message'] = 'Link inválido em '
        for rede_errada in errosInvalido:
           mensagem['message'] += rede_errada+' '
    elif len(errosNotFound) != 0:
        mensagem['status'] = False
        mensagem['message'] = 'A página não existe em '
        for rede_errada in errosNotFound:
            mensagem['message'] += rede_errada + ' '

    else:
        mensagem['status'] = True
        if canal.facebook != redes['facebook']:
            alterados.append('facebook')

        if canal.twitter != redes['twitter']:
            alterados.append('twitter')

        if canal.youtube != redes['youtube']:
            alterados.append('youtube')

        if canal.twitch != redes['twitch']:
            alterados.append('twitch')

        if canal.instagram != redes['instagram']:
            alterados.append('instagram')

        if canal.googleplus != redes['googleplus']:
            alterados.append('googleplus')
        if len(alterados) == 0:
            mensagem['message'] = 'Sem atualizações'
        else:
            mensagem['message'] = 'Atualização bem sucedida em '
            for rede in alterados:
                mensagem['message'] += rede+' '
    return mensagem


def certifica_link(redes):
    mensagem = {}
    ocorrencias = 0
    mensagem['message'] = 'Links incorretos em '
    mensagem['status'] = False
    for rede in redes:
        if rede not in redes[rede]:
            if redes[rede].isspace() or redes[rede] == '':
                continue
            else:
                mensagem['message'] += rede
                ocorrencias += 1
        if ocorrencias == 0:
            mensagem['status'] = True
    return mensagem


def setOrdemAudios(op,nome_canal):
    canal = Canal.objects.get(nome_canal=nome_canal)
    html = ''
    if op == 'recentes':
        audios = Audio.objects.filter(canal_proprietario=canal).order_by('data_publicacao').reverse()
    elif op == 'antigos':
        audios = Audio.objects.filter(canal_proprietario=canal).order_by('data_publicacao')
    elif op == 'populares':
        audios = Audio.objects.filter(canal_proprietario=canal).order_by('reproducoes')

    for audio in audios:
        html += '''<div class="col-md-3 mb-4"><div class="card">
                            <figure class="fig-capa-audio">
                                <a href="#"><img src="{}" class="card-img-top" alt="imagem do áudio"></a>
                                <figcaption class="fc-capa-audio">
                                    <center>
                                        <a href="#"><img src="/static/resources/icones/play.png" class="icon-play"/></a>
                                        <div class="dropdown more">
                                            <a data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                <img src="/static/resources/icones/more.png" class="icon-more"/>
                                            <div class="dropdown-menu more" aria-labelledby="dropdownMore">
                                                <a class="dropdown-item" href="#">Adicionar a playlist</a>
                                                <a class="dropdown-item" href="#">Compartilhar</a>
                                                <a class="dropdown-item" href="#">Editar</a>
                                                <a class="dropdown-item" href="#">Remover</a>
                                            </div>
                                            </a>
                                        </div>
                                    </center>
                                </figcaption>
                            </figure>

                            <div class="card-body">
                                <a href="#" class="audio-link"><h4 class="card-title audio-titul">{}</h4></a>
                                <div class="card-text">
                                    <p class="descript-thumb">{}</p>
                                    <p class="descript-thumb">
                                        <img src="/static/resources/icones/view.png" class="icon-view"/>
                                        {}</p>
                                    <p class="descript-thumb">{}</p>
                                </div>
                            </div>
                        </div>
                    </div>'''.format(audio.capa.url, audio.titulo, audio.canal_proprietario, audio.reproducoes, audio.data_publicacao.strftime('%d/%m/%y as %H:%M'))
    return html




def setOrdemPlaylists(op, canal):
    if op == "recentes":
        playlists = Playlist.objects.filter(canal=canal).order_by('ultima_atualizacao').reverse()
    elif op == 'antigos':
        playlists = Playlist.objects.filter(canal=canal).order_by('ultima_atualizacao')
    elif op == "mais audios":
        playlists = Playlist.objects.filter(canal=canal).order_by('numero_de_audios').reverse()
    elif op == "menos audios":
        playlists = Playlist.objects.filter(canal=canal).order_by('numero_de_audios')

    html = ""
    lista_audios = ""
    audios_ap = []
    playlists = ordena_pra_exibicao(playlists)
    for playlist in playlists:
        for audio in playlist.audios_apresentaveis:
            lista_audios += """ <li class="audio">
                                <strong class="time">3:40</strong>
                                <a href="#" class="titulo">
                                    <img src="/static/resources/icones/disc-white.png" class="thumb-audio"/>{}</a>
                            </li>""".format(audio.titulo)

        html += ''' <div class="col-md-6">
                    <div class="card">
                        <figure class="fig-capa-audio">
                            <a href="#"><img src="{}" class="card-img-top" alt=""></a>
                            <figcaption class="fc-capa-audio">
                                <center>
                                    <a href="#"><img src="/static/resources/icones/play.png" class="icon-play"/></a>
                                    <div class="dropdown more">
                                        <a data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                            <img src="/static/resources/icones/more.png" class="icon-more"/>
                                        <div class="dropdown-menu more" aria-labelledby="dropdownMore">
                                            <a class="dropdown-item" href="#">Editar</a>
                                            <a class="dropdown-item" href="#">Excluir</a>
                                            <a class="dropdown-item" href="#">Compartilhar</a>
                                        </div>
                                        </a>
                                    </div>
                                </center>
                            </figcaption>
                        </figure>

                        <div class="card-body">
                            <a href="#" class="audio-link"><h4 class="card-title audio-titul">{}</h4></a>
                            <div class="card-text">
                                <p class="descript-thumb">{}</p>
                                <p class="descript-thumb">
                                    <img src="/static/resources/icones/disc.ico" class="icon-view"/>
                                    {}</p>
                                <p class="descript-thumb last-update">{}</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 playlist">
                        <ul class="audio-list">
                            {}
                            <li class="playlist-more">
                                <center><a href="/channel/playlist_all/{}" class="btn playlist-link">Ver mais</a></center>
                            </li>
                        </ul>
                    </div>
                </div>'''.format(playlist.capa.url,
                                 playlist.nome,
                                 playlist.canal.nome_canal,
                                 playlist.numero_de_audios,
                                 playlist.ultima_atualizacao.strftime('%d/%m/%y as %H:%M'),
                                 lista_audios,
                                 playlist.id)
        lista_audios = ""
    return html



