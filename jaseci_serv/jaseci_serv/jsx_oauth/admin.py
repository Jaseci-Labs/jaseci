# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.utils.translation import gettext as _
# from jaseci_serv.base.models import User as base_user
# from jaseci_serv.jsx_oauth import models


# admin.site.unregister(base_user)


# class UserAdmin(BaseUserAdmin):
#     """
#     Customized user listing for admin page
#     """

#     ordering = ["time_created"]

#     list_display = ["email", "name", "time_created", "auth_provider"]
#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         (_("Personal Info"), {"fields": ("name",)}),
#         (_("Social Auth provider"), {"fields": ("auth_provider",)}),
#         (
#             _("Permissions"),
#             {
#                 "fields": (
#                     "is_active",
#                     "is_activated",
#                     "is_staff",
#                     "is_admin",
#                     "is_superuser",
#                 )
#             },
#         ),
#         (_("Important dates"), {"fields": ("last_login",)}),
#     )
#     add_fieldsets = (
#         (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
#     )


# admin.site.register(models.User, UserAdmin)
