import json
import base64
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


from dashboard.master.models import User
from .models import Messages

from fcom.settings import CHAT_UPLOADED_FILES_PATH, BASE_DIR, MEDIA_ROOT
from pathlib import Path


def save_file_to_disk(file_name, encoded):
    file_obj = base64.b64decode(encoded)

    file_full_path = Path(MEDIA_ROOT) / CHAT_UPLOADED_FILES_PATH / file_name
    with open(file_full_path, "wb") as f:
        f.write(file_obj)

    return file_name


class CustomerChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope["user"].id
        other_user_id = self.scope["url_route"]["kwargs"]["id"]
        if int(my_id) > int(other_user_id):
            self.room_name = f"{my_id}-{other_user_id}"
        else:
            self.room_name = f"{other_user_id}-{my_id}"

        await self.update_user_is_online(my_id, status=True)

        self.room_group_name = "chat_%s" % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        message_type = "text"
        file_name = None
        if "type" in data:
            header, encoded = data["dataURL"].split("base64,", 1)
            file_name = data["fileName"]
            file_name = save_file_to_disk(file_name, encoded)
            message_type = "file_upload"

        message = data["message"]
        username = data["username"]

        await self.save_message(username, self.room_group_name, message, file_name, message_type)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                "file_name" : file_name if file_name else "",
                "message_type" : message_type
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        user_id = event["username"]
        file_name = event["file_name"]
        message_type = event["message_type"]
        # user_obj = await self.get_userdetail(user_id)
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    #     'username' : user_obj.username,
                    "user_id": user_id,
                    "file_name" : file_name,
                    "message_type" : message_type
                }
            )
        )

    async def disconnect(self, code):
        my_id = self.scope["user"].id
        await self.update_user_is_online(user_id=my_id, status=False)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @database_sync_to_async
    def get_userdetail(self, user_id):
        user_obj = User.objects.get(id=user_id)
        return user_obj

    @database_sync_to_async
    def save_message(
        self, username, thread_name, message, uploaded_file=None, message_type="text"
    ):
        new_message = Messages.objects.create(
            sender=username,
            message=message,
            thread_name=thread_name,
            uploaded_file=uploaded_file,
            message_type=message_type
        )
        new_message.save()
        return

    @database_sync_to_async
    def update_user_is_online(self, user_id, status=False):
        user = User.objects.get(id=user_id)
        user.is_user_online = status
        user.save()

    async def write_uploaded_file(self, file_name, file_bytes):
        file_path = MEDIA_ROOT + "/chat-uploaded/" + file_name
        with open(file_path, "wb") as f:
            f.write(file_bytes)
