from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from accounts.models import CustomUser


class Admission(models.Model):
    date = models.DateTimeField(verbose_name="Date d'admission")
    code = models.CharField(max_length=25)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Utilisateur")

    def __str__(self):
        return self.code


class Group(models.Model):
    name = models.CharField(max_length=120, verbose_name="Nom du groupe")
    description = models.TextField(verbose_name="Description")
    status = models.CharField(max_length=25, verbose_name="Statut")
    date_don = models.DateTimeField()
    image = models.ImageField(null=True, blank=True, upload_to="images/groups/", verbose_name="Image du groupe")
    home_text = models.CharField(max_length=150, verbose_name="Texte d'affichage")
    banner_color = models.CharField(max_length=8, verbose_name="Couleur de la bannière")
    alias = models.CharField(max_length=120, verbose_name="Alias")
    slug = models.SlugField(null=True, unique=True, verbose_name="Slug")
    users = models.ManyToManyField(CustomUser, null=True, blank=True, verbose_name="Utilisateurs")
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Admission")

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
    start_date = models.DateTimeField(verbose_name="Date de début")
    end_date = models.DateTimeField(verbose_name="Date de fin")
    name = models.CharField(max_length=100, default="Activité sans nom", verbose_name="Nom de l'activité")
    description = models.TextField(max_length=500, verbose_name="Description")
    start_location = models.CharField(max_length=100, verbose_name="Lieu de départ")
    coordinates = models.CharField(max_length=30, verbose_name="Coordonnées")
    end_inscription_date = models.DateTimeField(verbose_name="Date de fin des inscriptions")
    end_location = models.CharField(max_length=100, verbose_name="Lieu de début")
    remarks = models.TextField(max_length=500, null=True, blank=True, verbose_name="Remarques")
    max_participants = models.PositiveIntegerField(verbose_name="Nombre maximum de participants")
    last_update = models.DateTimeField(verbose_name="Dernière mise à jour")
    slug = models.SlugField(null=True, unique=True, verbose_name="Slug")
    groups = models.ForeignKey(Group, null=True, on_delete=models.CASCADE, verbose_name="Groupes")
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, verbose_name="Utilisateur")

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
        self.slug = slugify(self.name) + slugify(self.user) + slugify(self.start_date)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Activities"


class Inscription(models.Model):
    date = models.DateTimeField(verbose_name="Date de l'inscription")
    remarks = models.TextField(max_length=500, null=True, blank=True, verbose_name="Remarques")
    presence = models.IntegerField(verbose_name="Présence")
    guests_number = models.IntegerField(verbose_name="Nombre de participants")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, verbose_name="Activité")

    def __str__(self):
        return self.remarks


class Donation(models.Model):
    amount = models.FloatField(verbose_name="Montant")
    date = models.DateTimeField(verbose_name="Date de la donation")
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name="Description")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, verbose_name="Utilisateur")
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True, verbose_name="Groupe")

    def __str__(self):
        return self.description
