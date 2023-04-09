from rest_framework import serializers
from .models import NewUser, Note


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "password",
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = NewUser
        fields = [
            'username',
            'picture',
        ]

    def get_picture(self, obj):
        return 'https://w7.pngwing.com/pngs/753/432/png-transparent-user-profile-2018-in-sight-user-conference-expo-business-default-business-angle-service-people-thumbnail.png'


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            "title",
            "body",
        ]


class NoteListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = [
            "title",
            "body",
            "created_on",
        ]
