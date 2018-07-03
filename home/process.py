from channel.models import Audio
from account.models import Canal


def GambiNice(canais):
    canalF = []
    for canal in canais:
        canal.playlist1 = Audio.objects.filter(canal_proprietario=canal).order_by('reproducoes')[:4]
        canal.playlist2 = Audio.objects.filter(canal_proprietario=canal).order_by('reproducoes')[4:8]
        canalF.append(canal)
    return canalF
