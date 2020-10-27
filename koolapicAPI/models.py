from django.db import models
from django.urls import reverse
# from django.core.validators import PositiveIntergerField


class Activity(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()
    start_location = models.TextField()
    coordinates = models.TextField()
    end_inscription_date = models.DateTimeField()
    end_location = models.TextField()
    remarks = models.TextField()
    max_participants = models.PositiveIntegerField()
    last_update = models.DateTimeField()

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("activity_detail", kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = "Activities"


class Group(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.TextField()
    date_don = models.DateTimeField()
    image = models.TextField()
    home_text = models.TextField()
    banner_color = models.TextField()
    alias = models.TextField()

    def __str__(self):
        return self.name


class Inscription(models.Model):
    date = models.DateTimeField()
    remark = models.TextField()
    presence = models.IntegerField()
    guests_number = models.IntegerField()

    def __str__(self):
        return self.remark


class Admission(models.Model):
    date = models.DateTimeField()
    code = models.TextField()

    def __str__(self):
        return self.code
