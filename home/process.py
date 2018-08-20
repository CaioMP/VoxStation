from channel.models import Audio
from account.models import Canal
from channel.process import get_tags

def GambiNice(canais):
    canalF = []
    for canal in canais:
        audio = Audio.objects.filter(canal_proprietario=canal)
        if audio.exists():
            canal.playlist1 = Audio.objects.filter(canal_proprietario=canal).order_by('reproducoes')[:4]
            canal.playlist2 = Audio.objects.filter(canal_proprietario=canal).order_by('reproducoes')[4:8]
            canalF.append(canal)
    return canalF


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

    if audios!= False:
        num_audios = audios.count()
    else:
        num_audios = 0
    if playlists != False:
        num_playlists = playlists.count()
    else:
        num_playlists = 0
    if canais != False:
        num_canais = canais.count()
    else:
        num_canais = 0

    total = num_canais+num_audios+num_playlists

    return total, num_playlists, num_audios, num_canais