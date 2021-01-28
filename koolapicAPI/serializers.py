from rest_framework import serializers
from koolapic.models import Activity, Invitation, Group, Inscription, Notification
from accounts.models import CustomUser


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Activity


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Invitation


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Group


class InscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Inscription


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = CustomUser


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Notification
