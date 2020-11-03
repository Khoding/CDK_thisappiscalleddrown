from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class CustomUser(AbstractUser):
    pass
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    tel_m = models.TextField(null=True)
    tel_p = models.TextField(null=True)
    address = models.TextField(null=True)
    npa = models.IntegerField(null=True)
    localite = models.TextField(null=True)
    last_login = models.DateTimeField(null=True)
    date_don = models.DateTimeField(null=True)
    inscription = models.DateTimeField(null=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)
