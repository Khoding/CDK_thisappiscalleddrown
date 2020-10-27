from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass
    first_name = models.TextField(max_length=45, null=True)
    last_name = models.TextField(max_length=45, null=True)
    email = models.EmailField(null=True)
    tel_m = models.TextField(null=True)
    tel_p = models.TextField(null=True)
    address = models.TextField(null=True)
    npa = models.IntegerField(null=True)
    localite = models.TextField(null=True)
    password = models.TextField(null=True)
    last_login = models.DateTimeField(null=True)
    date_don = models.DateTimeField(null=True)
    inscription = models.DateTimeField(null=True)

    def __str__(self):
        return self.username
