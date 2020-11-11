from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


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
    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return self.description

    def get_detail_url(self):
        return reverse("activity_detail", kwargs={'slug': self.slug})

    def get_add_url(self):
        return reverse("add_activity", kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse("update_activity", kwargs={'slug': self.slug})

    def get_confirm_delete_url(self):
        return reverse("activity_confirm_delete", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.description)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Activities"


class Group(models.Model):
    name = models.TextField()
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    status = models.TextField()
    date_don = models.DateTimeField()
    image = models.ImageField(null=True, blank=True, upload_to="images/groups/")
    home_text = models.TextField()
    banner_color = models.TextField(max_length=8)
    alias = models.TextField()
    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return self.name

    def get_detail_url(self):
        return reverse("group_detail", kwargs={'slug': self.slug})

    def get_add_url(self):
        return reverse("add_group", kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse("update_group", kwargs={'slug': self.slug})

    def get_confirm_delete_url(self):
        return reverse("group_confirm_delete", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


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
