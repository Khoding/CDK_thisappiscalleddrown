from django.contrib import admin
<<<<<<< HEAD
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404, HttpResponseServerError
from django.urls import path
=======
from django.urls import include, path
>>>>>>> master

from koolapic.views import IndexView


urlpatterns = [
    path('', IndexView.as_view()),
    path('index/', IndexView.as_view()),
    path('home/', IndexView.as_view()),
    path('api/', include('koolapicAPI.urls')),
]
