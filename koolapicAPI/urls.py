"""
URLs de l'application Koolapic API.
"""

from .views import InvitationViewSet, ActivityViewSet, GroupViewSet, InscriptionViewSet, UserViewSet, NotificationViewSet
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('invitation', InvitationViewSet, basename='invitation')
router.register('activity', ActivityViewSet, basename='activity')
router.register('group', GroupViewSet, basename='group')
router.register('inscription', InscriptionViewSet, basename='inscription')
router.register('user', UserViewSet, basename='user')
router.register('notification', NotificationViewSet, basename='notification')
urlpatterns = router.urls

