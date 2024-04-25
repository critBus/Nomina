from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import User


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    list_display = ("username", "email", "first_name", "is_staff")
    search_fields = ("username", "first_name", "last_name", "email")


admin.site.register(User, MyUserAdmin)
