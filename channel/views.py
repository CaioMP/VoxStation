from django.shortcuts import render, HttpResponse,redirect
from .forms import AudioForm
from .models import Audio


def myuploads(request):
    audio = Audio()
    if request.method == "POST":
        form = AudioForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save(commit=False)
            audio.titulo = form.cleaned_data['titulo']
            audio.audio = form.cleaned_data['audio']
            audio.descricao = form.cleaned_data['descricao']
            audio.capa = form.cleaned_data['capa']
            audio.likes = 1
            audio.deslikes = 1
            audio.audiencia = 0
            audio.reproducoes = 0
            audio.proprietario = request.user
            audio.save()

            return redirect('/')
        else:
            return HttpResponse(request, "erro de validação")
    form = AudioForm(instance=request.user)
    return render(request, "./channel/myUploads.html", {'form': form})


def channel(request, cod):
    return render(request, './channel/channel.html')


def playlist(request, cod):
    return render(request, './channel/playlists.html')


def about(request, cod):
    return render(request, './channel/about.html')


def uploads(request, cod):
    return render(request, './channel/uploads.html')
