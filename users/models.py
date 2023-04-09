from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import NewUserManager


class NewUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("First Name"), max_length=200)
    last_name = models.CharField(_("Last Name"), max_length=200)
    username = models.CharField(_("Username"), max_length=100, unique=True)
    date_joined = models.DateTimeField(_("Joined on"), auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=True)

    objects = NewUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username


class Note(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=200)
    body = models.TextField(_("Note"), null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def truncated_body(self):
        if len(self.body)>=20:
            return f'{self.body[0:20]}...'
        return self.body

    def __str__(self):
        return self.title
