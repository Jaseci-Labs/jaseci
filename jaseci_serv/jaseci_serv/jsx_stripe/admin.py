from django.contrib import admin
from .models import StripeVars


class StripeVarsAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = ("name", "value")
    search_fields = ["name", "value"]


admin.site.register(StripeVars, StripeVarsAdmin)
