from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
import time
# from dotenv import load_dotenv
from channels.exceptions import StopConsumer
import openai
import multiprocessing

# load_dotenv()

openai.api_key = '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'
messages = []

@sync_to_async
def get_ai_response(message):
    data = {
        "role":"user",
        "content":message,
    }
    messages.append(data)
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=messages,
    )
    return res['choices'][0]['message']['content']


class AIChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print(messages)

        self.room_id = self.scope["url_route"]["kwargs"].get("room_id")
        self.room_group_name = 'AI-Chat-room_'+str(self.room_id)
        print(self.room_group_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

    async def disconnect(self, code):
        print(code)
        messages.clear()
        print(messages)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
        p = multiprocessing.Process(target=get_ai_response)
        p.terminate()
        p.join()

        raise StopConsumer()

    async def receive(self, text_data):
        self.text_data_json = json.loads(text_data)
        self.message = self.text_data_json.get("message")
        print(self.message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"user_txt",
                "userText":self.message
            }
        )


        self.ai_response = await get_ai_response(message=self.message)
        print(self.ai_response)


        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"AI_response",
                "message" : self.ai_response,
            }
        )

    async def user_txt(self, event):
        self.user_text = event.get("userText")
        await self.send(text_data=json.dumps({
            "type":"user text",
            "userText":self.user_text,
        }))

    async def AI_response(self, event):
        self.message = event.get("message")

        await self.send(text_data=json.dumps({
            "type":"ai response",
            "message":self.message,
        }))
