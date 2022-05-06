from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from jaseci_serv.base import models


class UserAdmin(BaseUserAdmin):
    """
    Customized user listing for admin page
    """

    ordering = ["time_created"]
    list_display = ["email", "name", "time_created"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_activated",
                    "is_staff",
                    "is_admin",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )


admin.site.register(models.User, UserAdmin)


class JaseciObjectAdmin(admin.ModelAdmin):
    ordering = ["j_timestamp"]
    list_display = ("jid", "name", "j_type", "j_parent", "j_master", "j_timestamp")
    search_fields = [
        "jid",
        "name",
        "j_type",
        "j_parent",
        "j_master",
        "j_timestamp",
    ]


admin.site.register(models.JaseciObject, JaseciObjectAdmin)


class GlobalVarsAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = ("name", "value")
    search_fields = ["name", "value"]


admin.site.register(models.GlobalVars, GlobalVarsAdmin)
