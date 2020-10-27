from rest_framework import viewsets

from koolapicAPI.models import Activity, Admission, Group, Inscription
from accounts.models import CustomUser
from .serializers import AdmissionSerializer, ActivitySerializer, GroupSerializer, InscriptionSerializer, UserSerializer


class AdmissionViewSet(viewsets.ModelViewSet):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class InscriptionViewSet(viewsets.ModelViewSet):
    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
