from django import forms
from .models import Audio


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
            'descricao'
        ]
