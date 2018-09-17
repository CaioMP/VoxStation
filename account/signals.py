from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channel.models import Audio
User = get_user_model()


@receiver(post_save, sender=Audio)
def announce_new_audio(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "gossip", {"type": "user.gossip",
                       "event": "New Audio",
                       "titulo": instance.titulo,
                       "capa": instance.capa.url}
        )
        print("AQUIII! " + instance.capa.url),
