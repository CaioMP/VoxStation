from django.db import models
from account.models import MyUser, Anuncio, Canal
from datetime import datetime, timedelta
from tinytag import TinyTag
import os


class Tag(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField()

    def __str__(self):
        return self.nome


class Audio(models.Model):
    def audio_path(instance,filename):
        return "contas/user_{}/audios/{}".format(instance.proprietario.pk, filename)

    def capa_path(instance, filename):
        return "contas/user_{}/capas_audio/{}".format(instance.proprietario.pk, filename)

    def capa_playlist_path(instance, filename):
        return "contas/user_{}/capas_playlist/{}".format(instance.proprietario.pk, filename)

    def filename(self):
        return os.path.basename(self.audio.name)

    def get_duration(self):
        file = TinyTag.get('media/contas/user_{}/audios/{}'.format(self.proprietario.pk, self.filename()))
        duration = str(timedelta(seconds=file.duration))
        hours, minutes, miliseconds = duration.split(":")
        seconds, miliseconds = miliseconds.split(".")

        if hours == "0":
            if minutes.startswith("0"):
                duration = minutes[1:] + ":" + seconds
            else:
                duration = minutes + ":" + seconds
        else:
            if hours.startswith("0"):
                duration = hours[1:] + ":" + minutes + ":" + seconds
            else:
                duration = hours + ":" + minutes + ":" + seconds
        return duration

    data_publicacao = models.DateTimeField(default=datetime.now)
    estado = models.CharField(max_length=10, blank=True, null=True)
    visibilidade = models.CharField(max_length=11, blank=True, null=True)
    likes = models.ManyToManyField(MyUser, default=None, through="FeedLike", related_name="likes")
    deslikes = models.ManyToManyField(MyUser, default=None, through="FeedDesLike", related_name="deslikes")
    numero_likes = models.IntegerField(default=0)
    numero_deslikes = models.IntegerField(default=0)
    titulo = models.CharField(max_length=50)
    audio = models.FileField(upload_to=audio_path, null=True)
    capa = models.ImageField(upload_to=capa_path, null=True)
    duracao = models.CharField(max_length=15, blank=True, null=True)
    reproducoes = models.IntegerField()
    descricao = models.TextField(max_length=500, blank=True, null=True)
    categoria = models.CharField(max_length=15, blank=True, null=True)
    canal_proprietario = models.ForeignKey(Canal, on_delete=models.CASCADE, related_name="canal_proprietario", default=None, null=True)
    proprietario = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="proprietario", null=True)
    anuncios = models.ManyToManyField(Anuncio, blank=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    comentarista = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    conteudo = models.TextField()
    likes = models.IntegerField(null=True, default=0)
    deslikes = models.IntegerField(null=True, default=0)
    possui_resposta = models.IntegerField(default=0)
    data = models.DateTimeField(default=datetime.now)
    audio_comentado = models.ForeignKey(Audio, on_delete=models.CASCADE, default=None, null=True)

    class Meta:
        ordering = ['-data']

    def __unicode__(self):
        return str(self.comentarista)

    def __str__(self):
        comentario = str(self.comentarista) + " em " + str(self.audio_comentado)
        return comentario


class Resposta(models.Model):
    conteudo = models.TextField()
    likes = models.IntegerField(null=True, default=0)
    deslikes = models.IntegerField(null=True, default=0)
    data = models.DateTimeField(default=datetime.now)
    audio_comentado = models.ForeignKey(Audio, on_delete=models.CASCADE, default=None, null=True)
    comentarista = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    comentario_em_questao = models.ForeignKey(Comentario, on_delete=models.CASCADE)

    def __str__(self):
        comentario = str(self.comentarista) + " em " + str(self.audio_comentado)
        return comentario


class Playlist(models.Model):
    def playlist_capa_path(instance, filename):
        return "contas/user_{}/capas_de_playlists/{}".format(instance.proprietario.pk, filename)
    visibilidade_choices = (("publico", "público"), ("privada", "privada"))
    nome = models.CharField(max_length=50)
    audios = models.ManyToManyField(Audio)
    visibilidade = models.CharField(max_length=20, choices=visibilidade_choices, default="publico")
    proprietario = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='playlist_proprietario', default=None)
    canal = models.ForeignKey(Canal, related_name="canal_playlist", default=None, null=True, blank=True,  on_delete=models.CASCADE)
    ultima_atualizacao = models.DateTimeField(default=datetime.now)
    capa = models.ImageField(upload_to=playlist_capa_path, default=None, null=True)
    descricao = models.TextField(default=None, blank=True, null=True)
    numero_de_audios = models.IntegerField(default=1)
    reproducoes = models.IntegerField(default=0)

    def __str__(self):
        return self.nome


class FeedLike(models.Model):
    data_do_feed = models.DateTimeField(default=datetime.now)
    conta_feed = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="conta_do_like")
    Audio_feed = models.ForeignKey(Audio, on_delete=models.CASCADE, related_name="audio_do_like")

    def __str__(self):
        info = str(self.conta_feed) + " - " + str(self.Audio_feed)
        return info


class FeedDesLike(models.Model):
    data_do_feed = models.DateTimeField(default=datetime.now)
    conta_feed = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="conta_do_deslike")
    Audio_feed = models.ForeignKey(Audio, on_delete=models.CASCADE, related_name="audio_do_deslike")

    def __str__(self):
        info = str(self.conta_feed) + " - " + str(self.Audio_feed)
        return info


class AudioReport(models.Model):
    motivo = models.TextField()
    descricao = models.TextField()
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE, related_name="audio_reported")
    canal = models.ForeignKey(Canal, on_delete=models.CASCADE, related_name="canal_reported")
    usuario = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="user_reported")

    def __str__(self):
        return str(self.audio)


class Historico(models.Model):
    prop = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    audio = models.ManyToManyField(Audio)

    def __str__(self):
        return "Histórico de "+self.prop.username


class Favorito(models.Model):
    prop = models.ForeignKey(MyUser, on_delete=models.CASCADE,)
    audio = models.ManyToManyField(Audio, blank=True)

    def __str__(self):
        return "favoritos de "+self.prop.username


class NotificAudio(models.Model):
    user_notific = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="user_notific")
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE, related_name="audio_notific")
    visualized = models.BooleanField(default=False)

    def __str__(self):
        info = str(self.audio.pk) + " - " + str(self.user_notific)
        return info



