import openai
from rest_framework.decorators import api_view
from rest_framework.response import Response
from openai.api_resources.abstract.engine_api_resource import EngineAPIResource
import time
# from asgiref.sync import async_to_sync

openai.api_key = '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'



@api_view(["POST"])
def get_ai_response(req, *args, **kwargs):
    data = req.data.get("message")
    print(data)

    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=[
                {"role":"user","content":data}
            ]
        )
        message = res['choices'][0]['message']['content']
        return Response({"message":message}, status=200)
    except:
        return Response({"message":"error"}, status=500)

