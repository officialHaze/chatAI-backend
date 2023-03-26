from django.urls import path
from . import views



urlpatterns = [
    path('ai-response/', views.get_ai_response),
    path('transcribe-audio/', views.transcribe_audio)
]


