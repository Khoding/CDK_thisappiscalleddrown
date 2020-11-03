from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404, HttpResponseServerError
from django.urls import path
from django.urls import include, path
from django.urls import path, include

from koolapic.views import IndexView, ActivityListView, ActivityCreateView, ActivityDetailView
from koolapic.views import IndexView, SignUpView, KoolapicLoginView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('index/', IndexView.as_view()),
    path('home/', IndexView.as_view()),
    path('api/', include('koolapicAPI.urls')),
    path('activities/list', ActivityListView.as_view(), name="activity_list"),
    path('activites/<int:pk>/', ActivityDetailView.as_view(), name="activity_detail"),
    path('activities/add', ActivityCreateView.as_view()),
    path('', IndexView.as_view(), name='index'),
    path('index/', IndexView.as_view(), name='index'),
    path('home/', IndexView.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', KoolapicLoginView.as_view(), name='login'),
]
