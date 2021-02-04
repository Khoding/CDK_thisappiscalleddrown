from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

from ceffdevKAPIC.custom_settings import CONTRIBUTORS
from ceffdevKAPIC.settings import DEBUG


class CustomUser(AbstractUser):
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/", verbose_name="Photo de profil")
    bio = models.TextField(null=True, blank=True, verbose_name="Bio", help_text="A propos de vous", max_length=256)
    signup_date = models.DateTimeField(null=True, blank=True, verbose_name="Date d'inscription", help_text="Date d'inscription")
    donation_date = models.DateTimeField(null=True, blank=True, verbose_name="Date du dernier don", help_text="Date du dernier don")
    last_login = models.DateTimeField(auto_now_add=True, verbose_name="Dernier login", help_text="Date et heure du dernier login")
    locality = models.CharField(max_length=50, null=True, blank=True, verbose_name="Localité", help_text="Localité")
    npa = models.IntegerField(null=True, blank=True, verbose_name="NPA", help_text="NPA")
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name="Adresse", help_text="Adresse du domicile")
    tel_p = models.CharField(max_length=17, null=True, blank=True, verbose_name="Téléphone professionnel", help_text="Téléphone professionnel")
    tel_m = models.CharField(max_length=17, null=True, blank=True, verbose_name="Téléphone personnel", help_text="Téléphone personnel")
    slug = models.SlugField(null=True, verbose_name="Slug")

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if DEBUG:
            if self.is_contributor_superuser():
                self.is_superuser = True
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)

    def is_contributor_superuser(self):
        for contributor in CONTRIBUTORS:
            if self.email == contributor['email']:
                return True
        return False

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
