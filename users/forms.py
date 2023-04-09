from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import NewUser


class NewUserChangeForm(UserChangeForm):

    class Meta:
        model = NewUser
        fields = [
            "username",
        ]


class NewUserCreationForm(UserCreationForm):

    class Meta:
        model = NewUser
        fields = [
            "username",
        ]
