from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from dotenv import load_dotenv
import os
import openai

load_dotenv()


messages = []

@database_sync_to_async
def getResponse(message):
    # openai.api_key = os.environ.get('OPENAI_API_KEY')
    openai.api_key = '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'
    data = {
        "role":"user",
        "content":message,
    }
    messages.append(data)
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return res['choices'][0]['message']['content']


class AIChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        self.room_id = self.scope["url_route"]["kwargs"].get("room_id")
        print(self.room_id)
        self.room_group_name = 'AI-Chat-room_'+str(self.room_id)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

    async def disconnect(self, code):
        messages.clear()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"user_text",
                "userText":message
            }
        )

        ai_response = await getResponse(message)
        print(ai_response)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"AI_response",
                "message" : ai_response,
            }
        )

    async def user_text(self, event):
        user_text = event.get("userText")

        await self.send(text_data=json.dumps({
            "type":"user text",
            "userText":user_text,
        }))

    async def AI_response(self, event):
        message = event.get("message")

        await self.send(text_data=json.dumps({
            "type":"ai response",
            "message":message,
        }))
