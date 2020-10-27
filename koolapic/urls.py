from django.contrib import admin
from django.urls import include, path

from koolapic.views import IndexView, ActivityListView, ActivityCreateView, ActivityDetailView

urlpatterns = [
    path('', IndexView.as_view()),
    path('index/', IndexView.as_view()),
    path('home/', IndexView.as_view()),
    path('api/', include('koolapicAPI.urls')),
    path('activities/list', ActivityListView.as_view(), name="activity_list"),
    path('activites/<int:pk>/', ActivityDetailView.as_view(), name="activity_detail"),
    path('activities/add', ActivityCreateView.as_view()),
]
