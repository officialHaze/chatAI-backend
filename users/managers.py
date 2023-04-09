from django.contrib.auth.models import BaseUserManager


class NewUserManager(BaseUserManager):

    def create_user(self, first_name, last_name, username, password, **extra_fields):
        user = self.model(first_name=first_name, last_name=last_name, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)

        self.create_user(first_name=first_name, last_name=last_name, username=username, password=password, **extra_fields)
