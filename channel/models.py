from django.db import models
from account.models import MyUser, Anuncio, Canal


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

    data_publicacao = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=10, blank=True, null=True)
    visibilidade = models.CharField(max_length=11, blank=True, null=True)
    likes = models.ManyToManyField(MyUser, default=None, through="FeedLike", related_name="likes")
    deslikes = models.ManyToManyField(MyUser, default=None, through="FeedDesLike", related_name="deslikes")
    numero_likes = models.IntegerField(default=0)
    numero_deslikes = models.IntegerField(default=0)
    titulo = models.CharField(max_length=50)
    audio = models.FileField(upload_to=audio_path, blank=True, null=True)
    capa = models.ImageField(upload_to=capa_path, blank=True, null=True)
    duracao = models.CharField(max_length=15, blank=True, null=True)
    reproducoes = models.IntegerField()
    descricao = models.TextField(max_length=500)
    categoria = models.CharField(max_length=15, blank=True, null=True)
    canal_proprietario = models.ForeignKey(Canal, on_delete=models.CASCADE, related_name="canal_proprietario", default=None, null=True)
    proprietario = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="proprietario", null=True)
    anuncios = models.ManyToManyField(Anuncio, blank=True, null=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.titulo



class Playlist(models.Model):
    def playlist_capa_path(instance, filename):
        return "contas/user_{}/capas_de_playlists/{}".format(instance.proprietario.pk, filename)
    visibilidade_choices = (("publico", "público"), ("privada", "privada"))
    nome = models.CharField(max_length=50)
    audios = models.ManyToManyField(Audio)
    visibilidade = models.CharField(max_length=20, choices=visibilidade_choices, default="publico")
    proprietario = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='playlist_proprietario', default=None)
    canal = models.ForeignKey(Canal, related_name="canal_playlist", default=None, null=True, blank=True,  on_delete=models.CASCADE)
    ultima_atualizacao = models.DateTimeField(auto_now=True)
    capa = models.ImageField(upload_to=playlist_capa_path, default=None, null=True)
    descricao = models.TextField(default=None, blank=True, null=True)
    numero_de_audios = models.IntegerField(default=1)
    def __str__(self):
        return self.nome


class FeedLike(models.Model):
    data_do_feed = models.DateTimeField(auto_now=True)
    conta_feed = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="conta_do_like")
    Audio_feed = models.ForeignKey(Audio, on_delete=models.CASCADE, related_name="audio_do_like")


class FeedDesLike(models.Model):
    data_do_feed = models.DateTimeField(auto_now=True)
    conta_feed = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="conta_do_deslike")
    Audio_feed = models.ForeignKey(Audio, on_delete=models.CASCADE, related_name="audio_do_deslike")



