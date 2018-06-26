from django.shortcuts import render, HttpResponse,redirect
from .forms import AudioForm, TagForm
from .models import Audio,Tag
from account.models import Canal
from .process import tagprocess


def myuploads(request):
    audio = Audio()
    channels = Canal.objects.filter(proprietario=request.user)

    if request.method == "POST":
        tagform = TagForm(request.POST)
        form = AudioForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid() and tagform.is_valid():
            form.save(commit=False)
            audio.canal_proprietario = form.cleaned_data["canal_proprietario"]
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
            tagtext = tagform.cleaned_data['text']
            taglist = tagprocess(tagtext)
            for tagitem in taglist:
                query = Tag.objects.filter(nome=tagitem)
                if query.exists():
                    audio.tag.set(query)
                    audio.save()
                else:
                    query = Tag.objects.create(nome=tagitem)
                    query.save()
                    query = Tag.objects.filter(nome=tagitem)
                    audio.tag.set(query)
                    audio.save()

            return redirect('/')
        else:
            erro = True
            return render(request, "./channel/myuploads.html", {'form': form, 'channels': channels, "tagform": tagform, "erro": erro})
    tagform = TagForm()
    form = AudioForm(instance=request.user)
    return render(request, "./channel/myuploads.html", {'form': form, 'channels': channels, "tagform": tagform})


def channel(request, cod):
    return render(request, './channel/channel.html')


def playlist(request, cod):
    return render(request, './channel/playlists.html')


def about(request, cod):
    return render(request, './channel/about.html')


def uploads(request, cod):
    return render(request, './channel/uploads.html')
