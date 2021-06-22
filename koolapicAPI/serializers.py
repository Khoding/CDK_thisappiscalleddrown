"""
Sérialiseurs de l'API.
"""

from rest_framework import serializers

from accounts.models import CustomUser
from koolapic.models import Activity, Invitation, Group, Inscription, Notification


class ActivitySerializer(serializers.ModelSerializer):
    """
    Sérialiseur de la classe Activity.
    """

    class Meta:
        fields = "__all__"
        model = Activity


class InvitationSerializer(serializers.ModelSerializer):
    """
    Sérialiseur de la classe Invitation.
    """

    class Meta:
        fields = "__all__"
        model = Invitation


class GroupSerializer(serializers.ModelSerializer):
    """
    Sérialiseur de la classe Group.
    """

    class Meta:
        fields = "__all__"
        model = Group


class InscriptionSerializer(serializers.ModelSerializer):
    """
    Sérialiseur de la classe InscriptionActivity.
    """

    class Meta:
        fields = "__all__"
        model = Inscription


class UserSerializer(serializers.ModelSerializer):
    """
    Sérialiseur de la classe CustomUser.
    """

    class Meta:
        fields = "__all__"
        model = CustomUser


class NotificationSerializer(serializers.ModelSerializer):
    """
    Sérialiseur de la classe Notification.
    """

    class Meta:
        fields = "__all__"
        model = Notification
