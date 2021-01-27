import itertools
import secrets

from ckeditor.fields import RichTextField
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.urls import reverse, reverse_lazy

from accounts.models import CustomUser

import itertools
from datetime import datetime


def generate_vanity(min_length, max_length):
    length = secrets.choice(range(min_length, max_length))
    choices = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRTSUVWXYZ1234567890"
    vanity = ""

    for i in range(0, length):
        vanity += choices[secrets.choice(range(0, len(choices)))]
    return vanity


def generate_unique_vanity(min_length, max_length, model):
    vanity = generate_vanity(min_length, max_length)

    if model.objects.filter(slug=vanity).exists():
        return generate_unique_vanity(min_length, max_length, model)
    return vanity


class Group(models.Model):
    INVITATION_POLICY_CHOICES = [
        ('PU', 'Public'),  # Tout le monde peut rejoindre
        ('AA', 'Privé'),  # Les administrateurs doivent accepter les demandes
        ('OI', 'Sur invitation'),  # Un membre du groupe doit inviter la personne pour qu'elle puisse rejoindre
        ('OAI', 'Sur invitation par un admin'),  # Seuls les administrateurs peuvent inviter des personnes
    ]

    VISIBILITY_CHOICES = [
        ('IN', 'Invisible'),
        ('VI', 'Visible'),
    ]

    name = models.CharField(max_length=50, verbose_name="Nom du groupe")
    description = models.TextField(max_length=200, verbose_name="Description")
    visibility = models.CharField(max_length=25, verbose_name="Visibilité", choices=VISIBILITY_CHOICES, default='IN')
    invitation_policy = models.CharField(max_length=25, verbose_name="Politique des invitations", choices=INVITATION_POLICY_CHOICES, default='AA')
    image = models.ImageField(null=True, blank=True, upload_to="images/groups/", verbose_name="Image du groupe")
    banner_color = models.CharField(max_length=8, verbose_name="Couleur de la bannière")
    slug = models.SlugField(null=True, unique=True, verbose_name="Slug")
    members = models.ManyToManyField(CustomUser, related_name="members", related_query_name="member", verbose_name="Utilisateurs")
    admins = models.ManyToManyField(CustomUser, related_name="admins", related_query_name="admin", verbose_name="Administrateurs du groupe")
    banned_users = models.ManyToManyField(CustomUser, related_name="banned_users", related_query_name="banned_user", verbose_name="Utilisateurs bannis")

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
        self.slug = generate_unique_vanity(5, 15, Group)
        return super().save(*args, **kwargs)


class Activity(models.Model):
    name = models.CharField(max_length=32, default="Activité sans nom", verbose_name="Nom de l'activité")
    end_inscription_date = models.DateTimeField(verbose_name="Date de fin des inscriptions", blank=True, null=True)
    start_location = models.CharField(max_length=100, verbose_name="Lieu de départ")
    start_date = models.DateTimeField(verbose_name="Date de début")
    description = models.TextField(max_length=500, verbose_name="Description")
    end_location = models.CharField(max_length=100, verbose_name="Lieu de début")
    end_date = models.DateTimeField(verbose_name="Date de fin")
    remarks = RichTextField(max_length=500, null=True, blank=True, verbose_name="Remarques")  # Markdown
    max_participants = models.PositiveIntegerField(verbose_name="Nombre maximum de participants")
    last_update = models.DateTimeField(verbose_name="Dernière mise à jour", auto_now=True)
    slug = models.SlugField(max_length=255, null=True, unique=True, verbose_name="Slug")
    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE, verbose_name="Groupe")
    participants = models.ManyToManyField(CustomUser, related_name="participants", related_query_name="participant", verbose_name="Participants")

    def __str__(self):
        return self.name

    def get_detail_url(self):
        return reverse("koolapic:activity_detail", kwargs={'slug': self.slug})

    def get_clone_url(self):
        return reverse("koolapic:clone_activity", kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse("koolapic:update_activity", kwargs={'slug': self.slug})

    def get_confirm_delete_url(self):
        return reverse("koolapic:activity_confirm_delete", kwargs={'slug': self.slug})

    def is_past(self):
        return datetime.now() > self.end_date.replace(tzinfo=None)

    def save(self, *args, **kwargs):
        max_length = Activity._meta.get_field('slug').max_length
        self.slug = orig = slugify(self)[:max_length]
        for x in itertools.count(10):
            if self.id:
                if Activity.objects.filter(Q(slug=self.slug),
                                           Q(id=self.id),
                                           ).exists():
                    break
            if not Activity.objects.filter(slug=self.slug).exists():
                break

            # Truncate & Minus 1 for the hyphen.
            self.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)
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


class Notification(models.Model):
    SEVERITY_CHOICES = [
        ('DEBUG', 'Débogage'),
        ('INFO', 'Information'),
        ('WARNING', 'Avertissement'),
        ('DANGER', 'Danger'),
    ]

    STATUS = [
        ("U", "Non lue"),
        ("R", "Lue"),
        ("D", "Supprimée"),
    ]

    severity = models.CharField(max_length=10, default="INFO", verbose_name="Sévérité")
    title = models.CharField(max_length=100, verbose_name="Titre")
    description = models.CharField(max_length=250, verbose_name="Description")
    link = models.CharField(max_length=250, null=True, blank=True, verbose_name="Lien")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Utilisateur')
    date_sent = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Groupe")

    def __str__(self):
        return self.title


class Invitation(models.Model):
    ACCEPTATION_CHOICES = [
        ('ACC', 'Acceptée'),
        ('NAC', 'Non acceptée')
    ]

    date = models.DateTimeField(verbose_name="Date d'admission", auto_now=True)
    message = models.TextField(max_length=100, verbose_name="Message", blank=True, null=True)
    slug = models.SlugField(max_length=10, null=True, unique=True, verbose_name="Vanité d'invitation")
    sender = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, related_name="sender", verbose_name="Envoyeur")
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, related_name="receiver", verbose_name="Utilisateur")
    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE, verbose_name="Groupe")

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = generate_unique_vanity(5, 10, Invitation)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("koolapic:invitation", kwargs={'slug': self.slug})
