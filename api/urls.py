from django.urls import path, include
from . import views


urlpatterns = [
    path('ai-response/', views.get_ai_response),
    path('transcribe-audio/', views.transcribe_audio),
    path('server-connection/', views.establish_connection),

    #user model
    path('user/', include("users.urls")),
]


