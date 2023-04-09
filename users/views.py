from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserModelSerializer, UserDetailSerializer, NoteSerializer, NoteListSerializer
from .models import NewUser, Note
from social_django.models import UserSocialAuth
from dotenv import load_dotenv
import requests
import os


load_dotenv()


class RegisterUser(generics.CreateAPIView):
    serializer_class = UserModelSerializer
    permission_classes = [permissions.AllowAny]
    queryset = NewUser.objects.all()

    def perform_create(self, serializer):
        username = serializer.validated_data.get("username")
        first_name = serializer.validated_data.get("first_name")
        last_name = serializer.validated_data.get("last_name")
        password = serializer.validated_data.get("password")

        instance = NewUser.objects.create_user(username=username,
                                               first_name=first_name,
                                               last_name=last_name,
                                               password=password)

        print(instance)
        return instance


#notes list view
class NoteListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NoteListSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Note.objects.filter(user=user)
        return queryset


#delete note
class NoteDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NoteListSerializer
    lookup_field = "title"

    def get_queryset(self):
        user = self.request.user
        queryset = Note.objects.filter(user=user)
        return queryset


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def google_user_details(req, *args, **kwargs):
    user = req.user
    social = UserSocialAuth.objects.get(user=user, provider='google-oauth2')
    access_token = social.extra_data.get("access_token")

    try:
        response = requests.get(url=os.environ.get("GOOGLE_USER_DETAILS_ENDPOINT"), headers={
            "Authorization": f'Bearer {access_token}'
        })
        user_data = response.json()
    except:
        return Response({"details":"error getting user details"}, status=400)

    user_details = {
        "name":user_data['name'],
        "profile_picture": user_data['picture']
    }
    return Response(user_details, status=200)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def user_details(req, *args, **kwargs):
    user = req.user
    try:
        instance = NewUser.objects.get(username=user)
    except not isinstance:
        return Response({'detail':'error getting user information, probably the user does not exist'}, status=500)

    serializer = UserDetailSerializer(instance=instance)

    user_details = {
        "name":serializer.data['username'],
        "profile_picture": serializer.data['picture']
    }

    return Response(user_details, status=200)


#add note to the db
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_update_note(req, *args, **kwargs):
    user = req.user
    data = req.data
    serializer = NoteSerializer(data=data)
    if serializer.is_valid():
        title = serializer.validated_data.get("title")
        body = serializer.validated_data.get("body")
        queryset = Note.objects.filter(user=user,title=title)

        if not queryset:
            instance = Note.objects.create(user_id=user.id, title=title, body=body)
            print(f'instance = {instance}')
            return Response({'detail':'note created'}, status=200)

        queryset[0].body = body
        queryset[0].save()

        return Response({"deatail":"note updated"}, status=200)

    return Response({'detail':"error! please check the data"}, status=400)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def search_for_note(req, *args, **kwargs):
    user = req.user
    query_string_title = kwargs.get("title")
    if not query_string_title:
        return Response({"detail":"no query string provided to initiate search"}, status=400)
    found_notes = []

    notes = Note.objects.filter(user=user) #filter the notes by user

    #checking for every filtered note wether the string passed as query param is present in any of the filtered notes list
    for note in notes:
        if query_string_title in note.title:
            serialzier = NoteListSerializer(instance=note)
            found_notes.append(serialzier.data)

    return Response(found_notes)