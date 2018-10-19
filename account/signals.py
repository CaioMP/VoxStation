from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channel.models import Audio
from django.utils.dateformat import DateFormat
User = get_user_model()


@receiver(post_save, sender=Audio)
def announce_new_audio(sender, instance, created, **kwargs):
    if created:
        if instance.visibilidade != 'privado':
            channel_layer = get_channel_layer()

            df = DateFormat(instance.data_publicacao)
            data = df.format('d/m/y ') + "às " + df.format('H:i')
            link = str("/channel/audio/" + str(instance.pk))

            async_to_sync(channel_layer.group_send)(
                "notific", {
                    "type": "user.notific",
                    "event": "New Audio",
                    "link": link,
                    "titulo": instance.titulo,
                    "data": data,
                    "canal": instance.canal_proprietario.foto_canal.url,
                    "capa": instance.capa.url,
                    "id_canal": instance.canal_proprietario.pk
                }
            )
