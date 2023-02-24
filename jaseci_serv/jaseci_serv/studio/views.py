from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.template import TemplateDoesNotExist


def studio_index(request):
    try:
        return render(request, "studio/index.html")
    except TemplateDoesNotExist:
        return HttpResponseNotFound("Jaseci Studio is not installed.")


def studio_dashboard(request):
    try:
        return render(request, "studio/dashboard.html")
    except TemplateDoesNotExist:
        return HttpResponseNotFound("Jaseci Studio is not installed.")


def studio_graph_viewer(request):
    try:
        return render(request, "studio/graph-viewer.html")
    except TemplateDoesNotExist:
        return HttpResponseNotFound("Jaseci Studio is not installed.")


def studio_logs_viewer(request):
    try:
        return render(request, "studio/logs.html")
    except TemplateDoesNotExist:
        return HttpResponseNotFound("Jaseci Studio is not installed.")


def studio_architype(request):
    try:
        return render(request, "studio/architype.html")
    except TemplateDoesNotExist:
        return HttpResponseNotFound("Jaseci Studio is not installed.")


def studio_actions(request):
    try:
        return render(request, "studio/actions.html")
    except TemplateDoesNotExist:
        return HttpResponseNotFound("Jaseci Studio is not installed.")
