from django.contrib import admin
from django.urls import path

from koolapic.views import IndexView
from koolapicAPI.views import IndexAPIView

urlpatterns = [
    path('/', IndexAPIView.as_view()),
    path('', IndexAPIView.as_view()),
]
