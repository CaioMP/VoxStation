from channel.models import *
from channel.process import get_tags, ordena_pra_exibicao


def checkVisib(playlists=False, audios=False):
    if playlists:
        playlists_public = []

        for playlist in playlists.all():
            if playlist.visibilidade != 'privado':
                playlists_public.append(playlist)
        return playlists_public
    if audios:
        audios_public = []

        for audio in audios.all():
            if audio.visibilidade != 'privado':
                audios_public.append(audio)
        return audios_public


def orderAudios(canais):
    canalF = []
    for canal in canais:
        audio = Audio.objects.filter(canal_proprietario=canal)
        if audio.exists():
            canal.playlist1 = checkVisib(Audio.objects.filter(canal_proprietario=canal).order_by('-data_publicacao'))[:4]
            canal.playlist2 = checkVisib(Audio.objects.filter(canal_proprietario=canal).order_by('-data_publicacao'))[4:8]
            canalF.append(canal)
    return canalF


def searchclear(search, canal):
    audios = checkVisib(audios=Audio.objects.filter(titulo__contains=search, canal_proprietario=canal))
    if audios:
        audios_list = []
        for audio in audios:
            audios_list.append(str(audio.pk))
        return audios_list
    else:
        return False


def searchclear_playlists(search, canal):
    playlists = checkVisib(playlists=Playlist.objects.filter(nome__contains=search, canal=canal))
    if playlists:
        playlist_list = []
        for playlist in playlists:
            playlist_list.append(str(playlist.pk))
        return playlist_list
    else:
        return False


def checkExist(objeto):
    if objeto.exists():
        return objeto
    else:
        return False


def contaSeg(canais):
    for canal in canais:
        canal.num_seg = canal.seguidor.all().count()
        canal.num_audios = Audio.objects.filter(canal_proprietario=canal).count()
        canal.tags_main = get_tags(Audio.objects.filter(canal_proprietario=canal))[:2]
    return canais


def contaResultados(canais, audios, playlists):

    if audios:
        num_audios = len(audios)
    else:
        num_audios = 0
    if playlists:
        num_playlists = len(playlists)
    else:
        num_playlists = 0
    if canais:
        num_canais = canais.count()
    else:
        num_canais = 0

    total = num_canais + num_audios + num_playlists

    return total, num_playlists, num_audios, num_canais


def setOrdemAudiosSearch(audios):
    html = ''
    for audio in audios:
        html += '''<div class="col-12 col-sm-6 col-md-4 col-xl-3">
                            <div class="card canal audioBox">
                                <figure class="fig-capa-audio">
                                    <a href="#"><img src="{}" style="height: 100%;" class="card-img-top" alt=""></a>
                                    <figcaption class="fc-capa-audio">
                                        <center>
                                            <a href="#"><img src="/static/resources/icones/play.png" class="icon-play"/></a>
                                            <div class="dropdown more">
                                                <a data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                    <img src="/static/resources/icones/more.png" class="icon-more"/>
                                                <div class="dropdown-menu more" aria-labelledby="dropdownMore">
                                                    <a class="dropdown-item" href="#">Adicionar a playlist</a>
                                                    <a class="dropdown-item" href="#">Reproduzir depois</a>
                                                    <a class="dropdown-item" href="#">Compartilhar</a>
                                                    <a class="dropdown-item" href="#">Denunciar</a>
                                                </div>
                                                </a>
                                            </div>
                                        </center>
                                    </figcaption>
                                </figure>


                                <div class="card-body">
                                    <a href="#" class="audio-link"><h4 class="card-title">{}</h4></a>
                                    <div class="card-text">
                                        <!--Número de seguidores-->
                                        <p class="desc-audio">{}</p>
                                        <!--Número de áudios-->
                                        <p class="desc-audio">
                                            <img src="/static/resources/icones/view.png" class="icon-view views"/>{}
                                        </p>
                                        <p class="desc-audio">
                                            {}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>'''.format(audio.capa.url,
                                         audio.titulo,
                                         audio.canal_proprietario,
                                         audio.reproducoes,
                                         audio.data_publicacao.strftime('%d/%m/%y as %H:%M'))
    return html


def setOrdemPlaylistsSearch(playlists):
    html = ""
    lista_audios = ""
    playlists = ordena_pra_exibicao(playlists)
    for playlist in playlists:
        for audio in playlist.audios_apresentaveis:
            lista_audios += """ <li class="audio">
                                <strong class="time">3:40</strong>
                                <a href="#" class="titulo">
                                    <img src="/static/resources/icones/disc-white.png" class="thumb-audio"/>{}</a>
                            </li>""".format(audio.titulo)

        html += '''        <div class="col-md-6" style="margin-bottom: 1.8rem;">
                <div class="card">
                    <figure class="fig-capa-audio">
                        <a href="#"><img src="{}" style="height: 100%; border-radius: 4px 0 4px;"
                                         class="card-img-top" alt=""></a>
                        <figcaption class="fc-capa-audio">
                            <center>
                                <a href="#"><img src="/static/resources/icones/play.png" class="icon-play"/></a>
                                <div class="dropdown more">
                                    <a data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <img src="/static/resources/icones/more.png" class="icon-more"/>
                                    <div class="dropdown-menu more" aria-labelledby="dropdownMore">
                                        <a class="dropdown-item" href="#">Compartilhar</a>
                                        <a class="dropdown-item" href="#">Denunciar</a>
                                    </div>
                                    </a>
                                </div>
                            </center>
                        </figcaption>
                    </figure>

                    <div class="card-body info-playlist">
                        <a href="#" class="audio-link"><h4 class="card-title audio-titul">{}</h4></a>
                        <div class="card-text">
                            <p class="descript-thumb">{}</p>
                            <p class="descript-thumb">
                                <img src="/static/resources/icones/disc.ico" style="width: 1rem;" class="icon-view"/>
                                {}</p>
                            <p class="descript-thumb last-update">Última atualização <br>
                                {}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 playlist">
                    <ul class="audio-list">
                        {}
                        <li class="playlist-more">
                            <center><a href="playlist_all/{}" class="btn playlist-link">Ver mais</a></center>
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


def setOrdemCanais(canais):
    html = ""
    tags = ""
    for canal in canais:
        canal.tags = get_tags(Audio.objects.filter(canal_proprietario=canal))[:2]
        num_audios = Audio.objects.filter(canal_proprietario=canal).count()
        for tag in canal.tags:
            tags += "<div class='tag' style='margin-right: .5rem;'><a href='#'>#{}</a></div>".format(tag)

        html += """       <div class="col-6 col-sm-4 col-md-3">
                            <div class="card canal">
                                <a href="#">
                                    <img src="{}"
                                         class="card-img-top img-canal" alt="imagem do canal">
                                </a>

                                <div class="card-body desc-canal">
                                    <a href="#" class="audio-link"><h4 class="card-title">{}</h4></a>
                                    <div class="card-text">
                                        <!--Número de seguidores-->
                                        <p class="d-inline">
                                            <img src="/static/images/default-user.png" class="icon-view"
                                            rel="tooltip" data-toggle="tooltip" data-placement="top" title="Seguidores"/>
                                            {}
                                        </p>
                                        <!--Número de áudios-->
                                        <p class="d-inline">
                                            <img src="/static/resources/icones/disc.ico" style="margin-right: .3rem;width: auto;"
                                                 rel="tooltip" data-toggle="tooltip" data-placement="top" title="Áudios"
                                                 class="icon-view n-audios ml-3"/>{}
                                        </p>
                                        <div class="tags mt-3">
                                            {}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>""".format(canal.foto_canal.url,
                                         canal.nome_canal,
                                         canal.seguidor.all().count(),
                                         num_audios,
                                         tags)
        tags = ''
    return html
