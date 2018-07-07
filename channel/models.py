from django.db import models
from account.models import MyUser, Anuncio, Canal


class Tag(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField()


class Audio(models.Model):
    def audio_path(instance,filename):
        return "contas/user_{}/audios/{}".format(instance.proprietario.pk, filename)

    def capa_path(instance, filename):
        return "contas/user_{}/capas_audio/{}".format(instance.proprietario.pk, filename)

    data_publicacao = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=10)
    visibilidade = models.CharField(max_length=11)
    likes = models.IntegerField()
    deslikes = models.IntegerField()
    titulo = models.CharField(max_length=50)
    audio = models.FileField(upload_to=audio_path, blank=True, null=True)
    capa = models.ImageField(upload_to=capa_path, blank=True, null=True)
    duracao = models.CharField(max_length=15)
    reproducoes = models.IntegerField()
    descricao = models.TextField(max_length=500)
    categoria = models.CharField(max_length=15)
    canal_proprietario = models.ForeignKey(Canal, on_delete=models.CASCADE, related_name="canal_proprietario", default=None, null=True)
    proprietario = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="proprietario", null=True)
    anuncios = models.ManyToManyField(Anuncio)
    tag = models.ManyToManyField(Tag)
    feedback = models.ManyToManyField(MyUser, through="FeedBack", related_name="feedback")

    def __str__(self):
        return self.titulo


class Playlist(models.Model):
    nome = models.CharField(max_length=20)
    audios = models.ManyToManyField(Audio)
    proprietarios = models.ManyToManyField(MyUser)


class FeedBack(models.Model):
    tipo = models.IntegerField()
    conta_feed = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="conta_do_feed")
    Audio_feed = models.ForeignKey(Audio, on_delete=models.CASCADE, related_name="audio_do_feed")
