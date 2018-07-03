from django.shortcuts import render
from account.models import Canal
from channel.models import Audio,Anuncio
from .process import GambiNice

def IndexView(request):

    channel = Canal.objects.all()
    channels = GambiNice(channel)
    for channel in channels:
        print(channel.playlist1)
    return render(request, './home/index.html', {'logado': request.user.is_active, 'channels': channels})


def search(request):
    return render(request, './home/search.html')
