from rest_framework import serializers
from koolapicAPI.models import Activity, Admission, Group, Inscription
from accounts.models import CustomUser

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Activity

class AdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Admission

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
