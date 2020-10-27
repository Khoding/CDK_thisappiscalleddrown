from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    tel_m = models.TextField(null=True)
    tel_p = models.TextField(null=True)
    address = models.TextField(null=True)
    npa = models.IntegerField(null=True)
    localite = models.TextField(null=True)
    last_login = models.DateTimeField(null=True)
    date_don = models.DateTimeField(null=True)
    inscription = models.DateTimeField(null=True)

    def __str__(self):
        return self.username
