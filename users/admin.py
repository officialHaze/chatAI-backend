from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser, Note
from .forms import NewUserCreationForm, NewUserChangeForm
from django.utils.translation import gettext_lazy as _


class NewUserAdminView(UserAdmin):
    model = NewUser
    form = NewUserChangeForm
    add_form = NewUserCreationForm

    fieldsets = (
        (None, {"fields": ("username",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_admin",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "first_name", "last_name", "password1", "password2",
                           'is_staff', 'is_admin', 'is_superuser',
                           'is_active',),
            },
        ),
    )

    list_display = ("username", "first_name", "last_name", "date_joined", "id", "is_staff", "is_admin", "is_active",)
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    ordering = ('id',)


class AdminNoteView(admin.ModelAdmin):
    model = Note
    list_display = ("user", "title", Note.truncated_body, "id", "created_on",)
    list_filter = ("title", "created_on",)
    ordering = ("id",)


admin.site.register(NewUser, NewUserAdminView)
admin.site.register(Note, AdminNoteView)