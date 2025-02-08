import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.community_id = self.scope['url_route']['kwargs']['community_id']
        self.group_name = f"community_{self.community_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        message_id = data.get('message_id')
        send_id = data.get('send_id')
        community_id = data.get('community_id')
        contenttype = data.get('contenttype', 'text')
        sent_date = data.get('sent_date')
        chat_message = data.get('chat_message', "")
        media_content = data.get('media_content')
        media_caption = data.get('media_caption', "")

        # Adjust content type based on message content
        if media_content:
            contenttype = "image"

        # Broadcast the message
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message_id': message_id,
                'user_id': send_id,
                'community_id': community_id,
                'content_type': contenttype,
                'messagecontent': chat_message,
                'media_content': media_content,
                'media_caption': media_caption,
                'sent_date': sent_date,
            }
        )

    async def chat_message(self, event):
        # Send the formatted message to the WebSocket
        await self.send(text_data=json.dumps(event))
