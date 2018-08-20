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
