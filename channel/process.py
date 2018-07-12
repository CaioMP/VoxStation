from .models import Tag
from .models import Audio


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


def searchclear(search,canal):

    audio = Audio.objects.filter(titulo__contains=search, canal_proprietario=canal)
    if audio.exists():
        return audio
    else:
        return False

