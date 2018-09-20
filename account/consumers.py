from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import Canal


class NoseyConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        self.user = self.scope["user"]  # USUÁRIO QUE MANDA A NOTIFICAÇÃO
        print("USUARIO MANDANDO = " + str(self.user))
        await self.channel_layer.group_add("notific", self.channel_name)
        print(f"Added {self.channel_name} channel to notific")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notific", self.channel_name)
        print(f"Removed {self.channel_name} channel to notific")

    async def user_notific(self, event):
        self.user = self.scope["user"]  # USUÁRIO QUE RECEBE A NOTIFICAÇÃO

        channel_send = Canal.objects.get(pk=event['id_canal'])  # Canal que enviou o áudio
        if channel_send.users_notific:
            for user in channel_send.users_notific.all():
                if self.user == user:
                    print("USUARIO RECEPTOR = " + str(self.user))
                    await self.send_json(event)
                else:
                    print("O USUÁRIO", str(self.user), "NÃO RECEBE NOTIFICAÇÕES DE", str(channel_send.nome_canal))

