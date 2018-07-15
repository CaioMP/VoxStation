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

