"""
URLs de développements. Dans ce fichier se trouve les URL qui ne sont utilisées typiquement qu'à des fins de développements.
DOC : https://docs.djangoproject.com/en/3.1/topics/http/urls/
"""

from django.urls import path

from ceffdevKAPIC.dev_views import Error404View, Error400View, Error403View, Error500View
from ceffdevKAPIC.settings import DEBUG

app_name = 'dev'

if DEBUG:
    urlpatterns = [
        path('400', Error400View.as_view(), name='400'),
        path('403', Error403View.as_view(), name='403'),
        path('404', Error404View.as_view(), name='404'),
        path('500', Error500View.as_view(), name='500'),
    ]
else:
    urlpatterns = []
