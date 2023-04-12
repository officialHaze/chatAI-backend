import openai
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import time
import requests
from django.core.files.storage import FileSystemStorage
import os
from dotenv import load_dotenv
from rest_framework import permissions

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")
chat_completion_endpoint = os.environ.get('OPEN_AI_CHAT_COMPLETION_ENDPOINT')
ASSEMBLY_AI_API_TOKEN = os.environ.get("ASSEMBLY_AI_API_TOKEN")

prompt_array = [
    '\nHuman:hello\nAI:Hi, how may i assist you today',
    '\nHuman:who are you?\nAI:I am your friendly neighbourhood AI. I was created by OpenAI and is now being used in this web application developed by Moinak Dey',
    '\nHuman:what is your name?\nAI:You can call me anything you like'
    ]

ai_res = None

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def get_ai_response(req, *args, **kwargs):
    data = req.data.get("message")
    prompt = data[-1]['content'] #getting the last object from the array to get hold of the last message user sent
    new_prompt = [*prompt_array, f'\nHuman:{prompt}\nAI: '] #takes the prompt array containing user message and ai response then appending the new user prompt to it for the AI to respond to

    res = openai.Completion.create(
        model="text-davinci-003",
        prompt=
        f"The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. {new_prompt}",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    ai_res = res['choices'][0]['text'] #getting the AI response
    prompt_array.append(f'\nHuman:{prompt}\nAI:{ai_res}') #appending it to the prompt_array(updating the previous prompt array)
    return Response({"message":ai_res}, status=200)



@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def transcribe_audio(req, *args, **kwargs):
    audio_file = req.FILES.get("audio_file")
    print(audio_file)
    chunk_size = 5242880
    upload_endpoint = os.environ.get('ASSEMBLY_AI_UPLOAD_ENDPOINT')
    transcript_endpoint = os.environ.get('ASSEMBLY_AI_TRANSCRIPT_ENDPOINT')

    fs = FileSystemStorage()
    audio_file_path = fs.save(audio_file.name, audio_file)

    #opening the saved file to read the byte data
    with fs.open(audio_file_path, 'rb') as _file:
        audio_data = _file.read(chunk_size)

    #sending post request to assembly ai with audio data to upload it
    try:
        response = requests.post(url=upload_endpoint, data=audio_data, headers={'authorization':ASSEMBLY_AI_API_TOKEN})
        upload_url = response.json().get('upload_url')
    except:
        return Response({"detail": "there was an error uploading the audio file"}, status=400)

    #posting the uploaded url to assembly ai for transcripting
    try:
        response = requests.post(
            url=transcript_endpoint,
            json={"audio_url":upload_url},
            headers={'authorization':ASSEMBLY_AI_API_TOKEN})

        transcript_id = response.json().get('id')
    except:
       return Response({"detail": "there was an error transcripting the audio data"}, status=400)

    #making GET request to assembly ai api every second unless the status shows completed
    while True:
        response = requests.get(
            url=transcript_endpoint + f'/{transcript_id}',
            headers={'authorization':ASSEMBLY_AI_API_TOKEN})

        status = response.json().get("status")
        if status == "completed":
            transcribed_text = response.json()['text']
            fs.delete(audio_file_path)
            break
        time.sleep(1)

    return Response({"detail":transcribed_text}, status=200)


#establish connection with client
@api_view(["GET"])
def establish_connection(req, *args, **kwargs):
    return Response({"detail":"connection established"}, status=200)
