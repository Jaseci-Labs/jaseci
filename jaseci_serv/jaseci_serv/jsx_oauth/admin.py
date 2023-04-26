from django import forms
from django.contrib import admin

from .models import SocialApp, LegacySocialApp


class SocialAppForm(forms.ModelForm):
    class Meta:
        model = SocialApp
        exclude = []
        widgets = {
            "client_id": forms.TextInput(attrs={"size": "100"}),
            "key": forms.TextInput(attrs={"size": "100"}),
            "secret": forms.TextInput(attrs={"size": "100"}),
        }


class SocialAppAdmin(admin.ModelAdmin):
    form = SocialAppForm
    list_display = ("id", "name", "provider")


admin.site.unregister(LegacySocialApp)
admin.site.register(SocialApp, SocialAppAdmin)
