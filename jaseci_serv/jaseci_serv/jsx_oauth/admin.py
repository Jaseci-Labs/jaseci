from django import forms
from django.contrib import admin
from .models import InternalClient
from allauth.socialaccount.models import SocialApp


class SocialAppChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, social_app):
        return f"{social_app.name}: {social_app.client_id}"


class InternalClientForm(forms.ModelForm):
    social_app = SocialAppChoiceField(queryset=SocialApp.objects.all())

    class Meta:
        model = InternalClient
        fields = ["name", "client_id"]


class InternalClientAdmin(admin.ModelAdmin):
    form = InternalClientForm
    list_display = ("name", "client_id", "social_app", "social_app_client_id")

    def social_app_client_id(self, internal_client):
        return internal_client.social_app.client_id


admin.site.register(InternalClient, InternalClientAdmin)
