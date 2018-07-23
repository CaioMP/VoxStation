from django import forms
from .models import Audio,Playlist


class AudioForm(forms.ModelForm):
    audio = forms.FileField(widget=forms.FileInput)
    capa = forms.ImageField(widget=forms.FileInput)
    titulo = forms.CharField()
    descricao = forms.Textarea()

    class Meta:
        model = Audio
        fields = [
            'audio',
            'capa',
            'titulo',
            'descricao',
            'canal_proprietario'
        ]


class TagForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)


class SearchChannelAudioForm(forms.Form):
    text = forms.CharField()


class PlaylistForm(forms.ModelForm):
    nome = forms.CharField()
    capa = forms.ImageField()

    class Meta:
        model = Playlist
        fields = [
            'nome'
        ]


class capaForm(forms.ModelForm):
    capa = forms.ImageField()

    class Meta:
        model = Playlist
        fields = [
            'capa'
        ]



