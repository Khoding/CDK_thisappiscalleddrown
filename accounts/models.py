from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save

from utils.db_utils import generate_unique_vanity


def give_default_username(sender, instance, *args, **kwargs):
    """Ajoute un nom d'utilisateur unique par défaut en récupérant son slug."""

    instance.username = instance.slug


class CustomUser(AbstractUser):
    """Classe représentant le modèle des utilisateurs, ainsi que du profil."""

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'

    email = models.EmailField(max_length=255, unique=True, verbose_name='Adresse e-mail')

    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/", verbose_name="Photo de profil")
    bio = models.TextField(null=True, blank=True, verbose_name="Bio", help_text="A propos de vous", max_length=256)
    donation_date = models.DateTimeField(null=True, blank=True, verbose_name="Date du dernier don", help_text="Date du dernier don")
    last_login = models.DateTimeField(auto_now_add=True, verbose_name="Dernier login", help_text="Date et heure du dernier login")
    locality = models.CharField(max_length=50, null=True, blank=True, verbose_name="Localité", help_text="Localité")
    npa = models.IntegerField(null=True, blank=True, verbose_name="NPA", help_text="NPA")
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name="Adresse", help_text="Adresse du domicile")
    tel_p = models.CharField(max_length=17, null=True, blank=True, verbose_name="Téléphone professionnel", help_text="Téléphone professionnel")
    tel_m = models.CharField(max_length=17, null=True, blank=True, verbose_name="Téléphone personnel", help_text="Téléphone personnel")
    slug = models.SlugField(null=True, verbose_name="Slug")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_vanity(5, 10, CustomUser)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'utilisateur'
        verbose_name_plural = 'utilisateurs'


pre_save.connect(give_default_username, sender=CustomUser)  # Signal se déclanchant avant l'enregistrement dans la base de donnée
