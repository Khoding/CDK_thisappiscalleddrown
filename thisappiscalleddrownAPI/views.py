"""
Vues de l'application thisappiscalleddrown API.
"""

from rest_framework import viewsets

from accounts.models import CustomUser
from thisappiscalleddrown.models import Activity, Invitation, Group, Inscription, Notification
from .serializers import (
    InvitationSerializer,
    ActivitySerializer,
    GroupSerializer,
    InscriptionSerializer,
    UserSerializer,
    NotificationSerializer,
)


class InvitationViewSet(viewsets.ModelViewSet):
    """
    Viewset de la classe Invitation.
    """

    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    """
    Viewset de la classe Activity.
    """

    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    Viewset de la classe Group.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class InscriptionViewSet(viewsets.ModelViewSet):
    """
    Viewset de la classe Inscription.
    """

    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset de la classe CustomUser.
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    Viewset de la classe Notification.
    """

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
