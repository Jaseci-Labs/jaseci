from django.urls import path
from . import api

app_name = 'jac_api'

urlpatterns = []

for i in dir(api):
    if (i.startswith('api_')):
        urlpatterns.append(
            path(f'jac/{i[4:]}', getattr(api, i).as_view(), name=f'{i[4:]}'))
