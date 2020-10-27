from django.contrib import admin
from django.urls import include, path

from koolapic.views import IndexView

urlpatterns = [
    path('', IndexView.as_view()),
    path('index/', IndexView.as_view()),
    path('home/', IndexView.as_view()),
    path('api/', include('koolapicAPI.urls')),
]
