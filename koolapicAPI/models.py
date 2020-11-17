from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from accounts.models import CustomUser


class Admission(models.Model):
    date = models.DateTimeField()
    code = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.code


class Group(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.TextField()
    date_don = models.DateTimeField()
    image = models.ImageField(null=True, blank=True, upload_to="images/groups/")
    home_text = models.TextField()
    banner_color = models.TextField(max_length=8)
    alias = models.TextField()
    slug = models.SlugField(null=True, unique=True)
    users = models.ManyToManyField(CustomUser)
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_detail_url(self):
        return reverse("koolapic:group_detail", kwargs={'slug': self.slug})

    def get_add_url(self):
        return reverse("koolapic:add_group", kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse("koolapic:update_group", kwargs={'slug': self.slug})

    def get_confirm_delete_url(self):
        return reverse("koolapic:group_confirm_delete", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


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
    groups = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    def get_detail_url(self):
        return reverse("koolapic:activity_detail", kwargs={'slug': self.slug})

    def get_add_url(self):
        return reverse("koolapic:add_activity", kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse("koolapic:update_activity", kwargs={'slug': self.slug})

    def get_confirm_delete_url(self):
        return reverse("koolapic:activity_confirm_delete", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.description)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Activities"


class Inscription(models.Model):
    date = models.DateTimeField()
    remark = models.TextField()
    presence = models.IntegerField()
    guests_number = models.IntegerField()
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.remark
