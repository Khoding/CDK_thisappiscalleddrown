from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    tel_m = models.TextField(max_length=17, null=True, blank=True, verbose_name="Téléphone personnel", help_text="Téléphone personnel")
    tel_p = models.TextField(max_length=17, null=True, blank=True, verbose_name="Téléphone professionnel", help_text="Téléphone professionnel")
    address = models.TextField(max_length=50, null=True, blank=True, verbose_name="Adresse", help_text="Adresse du domicile")
    npa = models.IntegerField(null=True, blank=True, verbose_name="NPA", help_text="NPA")
    localite = models.TextField(max_length=50, null=True, blank=True, verbose_name="Localité", help_text="Localité")
    last_login = models.DateTimeField(auto_now_add=True, verbose_name="Dernier login", help_text="Dernier login")
    donation_date = models.DateTimeField(null=True, blank=True, verbose_name="Date du dernier don", help_text="Date du dernier")
    signup_date = models.DateTimeField(null=True, blank=True, verbose_name="Date d'inscription", help_text="Date d'inscription")

    def __str__(self):
        return self.username
