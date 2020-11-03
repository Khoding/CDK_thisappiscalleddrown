from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404, HttpResponseServerError
from django.urls import path
from django.urls import include, path

from koolapic.views import IndexView, ActivityListView, ActivityCreateView, ActivityDetailView


urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('index/', IndexView.as_view()),
    path('home/', IndexView.as_view()),
    path('api/', include('koolapicAPI.urls')),
    path('activities/list', ActivityListView.as_view(), name="activity_list"),
    path('activities/<slug:slug>/', ActivityDetailView.as_view(), name="activity_detail"),
    path('activities/add', ActivityCreateView.as_view(), name="add_activity"),
]
