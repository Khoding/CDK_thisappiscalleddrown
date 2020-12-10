from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404, HttpResponseServerError
from django.urls import path
from django.urls import include, path

from koolapic.views import ActivityListView, ActivityCreateView, ActivityDetailView, ActivityUpdateView, ActivityDeleteView, \
    GroupListView, GroupCreateView, GroupDetailView, GroupUpdateView, GroupDeleteView
from koolapic.views import IndexView, HomeView

app_name = 'koolapic'

urlpatterns = [
    path('app/', IndexView.as_view(), name='home'),
    path('', HomeView.as_view(), name='homepage'),

    path('activities/', ActivityListView.as_view(), name="activity_list"),
    path('activities/<slug:slug>/', ActivityDetailView.as_view(), name="activity_detail"),
    path('activities/add', ActivityCreateView.as_view(), name="add_activity"),
    path('activities/<slug:slug>/update/', ActivityUpdateView.as_view(), name="update_activity"),
    path('activities/<slug:slug>/confirm_delete/', ActivityDeleteView.as_view(), name="activity_confirm_delete"),

    path('groups/', GroupListView.as_view(), name="group_list"),
    path('groups/<slug:slug>/', GroupDetailView.as_view(), name="group_detail"),
    path('groups/add', GroupCreateView.as_view(), name="add_group"),
    path('groups/<slug:slug>/update/', GroupUpdateView.as_view(), name="update_group"),
    path('groups/<slug:slug>/confirm_delete/', GroupDeleteView.as_view(), name="group_confirm_delete"),
]
