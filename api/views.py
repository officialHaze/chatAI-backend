import openai
from rest_framework.decorators import api_view
from rest_framework.response import Response
import time
import requests
from django.core.files.storage import FileSystemStorage


openai.api_key = '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'
ASSEMBLY_AI_API_TOKEN = 'c34b245fee6a4332872bb093421017c1'


@api_view(["POST"])
def get_ai_response(req, *args, **kwargs):
    data = req.data.get("message")

    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=data
        )
        message = res['choices'][0]['message']['content']
        return Response({"message":message}, status=200)
    except:
        return Response({"message":"error"}, status=500)


@api_view(["POST"])
def transcribe_audio(req, *args, **kwargs):
    audio_file = req.FILES.get("audio_file")
    chunk_size = 5242880
    upload_endpoint = 'https://api.assemblyai.com/v2/upload'
    transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'

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
