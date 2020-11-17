from django.contrib import admin
from django.urls import path

from .views import AdmissionViewSet, ActivityViewSet, GroupViewSet, InscriptionViewSet, UserViewSet
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('admission', AdmissionViewSet, basename='admission')
router.register('activity', ActivityViewSet, basename='activity')
router.register('group', GroupViewSet, basename='group')
router.register('inscription', InscriptionViewSet, basename='inscription')
router.register('user', UserViewSet, basename='user')
urlpatterns = router.urls

