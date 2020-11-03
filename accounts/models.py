from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class CustomUser(AbstractUser):
    pass
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    signup_date = models.DateTimeField(null=True, blank=True, verbose_name="Date d'inscription", help_text="Date d'inscription")
    donation_date = models.DateTimeField(null=True, blank=True, verbose_name="Date du dernier don", help_text="Date du dernier")
    last_login = models.DateTimeField(auto_now_add=True, verbose_name="Dernier login", help_text="Dernier login")
    localite = models.TextField(max_length=50, null=True, blank=True, verbose_name="Localité", help_text="Localité")
    npa = models.IntegerField(null=True, blank=True, verbose_name="NPA", help_text="NPA")
    address = models.TextField(max_length=50, null=True, blank=True, verbose_name="Adresse", help_text="Adresse du domicile")
    tel_p = models.TextField(max_length=17, null=True, blank=True, verbose_name="Téléphone professionnel", help_text="Téléphone professionnel")
    tel_m = models.TextField(max_length=17, null=True, blank=True, verbose_name="Téléphone personnel", help_text="Téléphone personnel")
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)
