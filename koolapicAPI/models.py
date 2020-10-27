from django.db import models


class Activity(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()
    start_location = models.TextField()
    coordinates = models.TextField()
    end_inscription_date = models.DateTimeField()
    end_location = models.TextField()
    remarks = models.TextField()
    max_participants = models.IntegerField()
    last_update = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Activities"


# class Group pas faite parce qu'on pourrait utiliser l'api Facebook pour les gérer (prendre le nom, la banière, etc depuis Facebook)


class Group(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.TextField()
    date_don = models.DateTimeField()
    image = models.TextField()
    home_text = models.TextField()
    banner_color = models.TextField()
    alias = models.TextField()


class Inscription(models.Model):
    date = models.DateTimeField()
    remark = models.TextField()
    presence = models.IntegerField()
    guests_number = models.IntegerField()


class Admission(models.Model):
    date = models.DateTimeField()
    code = models.TextField()
