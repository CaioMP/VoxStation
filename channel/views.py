from django.shortcuts import render, HttpResponse,redirect, reverse
from .forms import AudioForm, TagForm,SearchChannelAudioForm
from .models import Audio,Tag
from account.models import Canal
from .process import tagprocess, getaudios, searchclear


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
            return render(request, "./channel/myuploads.html", {'form': form, 'channels': channels, 'logado': request.user.is_active,
                                                                "tagform": tagform, "erro": erro})
    tagform = TagForm()
    form = AudioForm(instance=request.user)
    return render(request, "./channel/myuploads.html", {'form': form, 'channels': channels,
                                                        "tagform": tagform, 'logado': request.user.is_active})


def channel(request, nome):
    chan = getaudios(Canal.objects.get(nome_canal=nome))

    return render(request, './channel/channel.html', {'chan': chan})


def playlist(request,nome):
    return render(request, './channel/playlists.html')


def about(request, nome):
    return render(request, './channel/about.html')


def uploads(request, nome):
    contexto= {}
    canal = Canal.objects.get(nome_canal=nome)
    if request.method == 'POST':
        search_form = SearchChannelAudioForm(request.POST)

        if search_form.is_valid():
            search = search_form.cleaned_data['text']
            audios = searchclear(search,canal)
            contexto['audios'] = audios
            contexto['chan'] = canal
            contexto['form_aud'] = SearchChannelAudioForm()
            return render(request, './channel/uploads.html', contexto)
        else:
            contexto['chan'] = canal
            contexto['erro'] = True
            contexto['form_aud'] = SearchChannelAudioForm()
            return render(request, './channel/uploads.html', contexto)
    else:
        audios = Audio.objects.filter(canal_proprietario=canal).order_by('data_publicacao').reverse()
        contexto['audios'] = audios
        contexto['chan'] = canal
        contexto['form_aud'] = SearchChannelAudioForm()
        return render(request, './channel/uploads.html', contexto)


def partner(request, nome):
    return render(request, './channel/similar.html')
