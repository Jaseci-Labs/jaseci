from django.shortcuts import render
from django.conf import settings


def serve_html(request):
    return render(request, "studio/index.html")
