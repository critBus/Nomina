from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.utils.safestring import mark_safe

from apps.users.models import User


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    def grupos(self, obj):
        nombres = [v.name for v in Group.objects.filter(permissions=obj)]
        return mark_safe("<br>\n".join(nombres))

    list_display = ("id", "name", "grupos")
    search_fields = (
        "id",
        "name",
    )
    list_filter = ("group__name",)
    ordering = (
        "-id",
        "name",
    )
    list_display_links = (
        "id",
        "name",
    )
    # fieldsets = ((None, {"fields": ("name",)}),)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class MyUserAdmin(UserAdmin):
    add_form_template = "admin/auth/user/add_form.html"
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (
            "Información Personal",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Permisos",
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
