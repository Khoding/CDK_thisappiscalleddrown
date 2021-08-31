from datetime import datetime
from django.db import models
from django.urls import reverse, reverse_lazy

from accounts.models import CustomUser
from utils.db_utils import generate_unique_vanity


class Group(models.Model):
    """
    Modèle représentant un groupe Koolapic.
    """

    name = models.CharField(max_length=50, verbose_name="Nom du groupe")
    description = models.TextField(max_length=200, verbose_name="Description")
    image = models.ImageField(
        null=True, blank=True, upload_to="images/groups/", verbose_name="Image du groupe")
    banner_color = models.CharField(
        max_length=8, verbose_name="Couleur de la bannière")
    slug = models.SlugField(null=True, unique=True, verbose_name="Slug")

    members = models.ManyToManyField(CustomUser, related_name="members", related_query_name="member",
                                     verbose_name="Utilisateurs")
    admins = models.ManyToManyField(CustomUser, related_name="admins", related_query_name="admin",
                                    verbose_name="Administrateurs du groupe")

    website = models.TextField(
        max_length=100, null=True, blank=True, verbose_name="Site web")

    class Meta:
        verbose_name = 'groupe'
        verbose_name_plural = 'groupes'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Fonction apelée à la sauvegarde du groupe.
        """
        if not self.slug:
            self.slug = generate_unique_vanity(5, 10, Group)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("koolapic:group_detail", kwargs={'slug': self.slug})

    def get_add_url(self):
        return reverse("koolapic:add_group", kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse("koolapic:update_group", kwargs={'slug': self.slug})

    def get_confirm_delete_url(self):
        return reverse("koolapic:group_confirm_delete", kwargs={'slug': self.slug})


class Activity(models.Model):
    """
    Modèle représentant une activité.
    """

    name = models.CharField(
        max_length=32, default="Activité sans nom", verbose_name="Nom de l'activité")
    description = models.TextField(max_length=500, verbose_name="Description")
    creator = models.ForeignKey(
        CustomUser, null=True, blank=True, verbose_name="Créateur", on_delete=models.CASCADE)

    remarks = models.TextField(
        max_length=500, null=True, blank=True, verbose_name="Remarques")
    max_participants = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Max de participants")

    start_location = models.CharField(
        max_length=100, null=True, verbose_name="Lieu de départ")
    start_date = models.DateTimeField(verbose_name="Date de début")

    end_location = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Lieu de fin")
    end_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Date de fin")

    last_update = models.DateTimeField(
        verbose_name="Dernière mise à jour", auto_now=True)
    participants = models.ManyToManyField(CustomUser, related_name="participants", related_query_name="participant",
                                          verbose_name="Participants", blank=True)
    slug = models.SlugField(max_length=255, null=True,
                            unique=True, verbose_name="Slug")
    group = models.ForeignKey(
        Group, null=True, on_delete=models.CASCADE, verbose_name="Groupe")

    class Meta:
        verbose_name = 'activité'
        verbose_name_plural = 'activités'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Fonction apelée à la sauvegarde de l'activité.
        """
        if not self.slug:
            self.slug = generate_unique_vanity(5, 10, Activity)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("koolapic:activity_detail", kwargs={'slug': self.slug})

    def get_clone_url(self):
        return reverse("koolapic:clone_activity", kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse("koolapic:update_activity", kwargs={'slug': self.slug})

    def get_confirm_delete_url(self):
        return reverse("koolapic:activity_confirm_delete", kwargs={'slug': self.slug})


class Inscription(models.Model):
    """
    Modèle représentant une inscription à une activité.
    """

    date = models.DateTimeField(
        verbose_name="Date de l'inscription", default=datetime.now)
    remarks = models.TextField(
        max_length=500, null=True, blank=True, verbose_name="Remarques")
    presence = models.BooleanField(verbose_name="Présence", default=True)
    guests_number = models.PositiveIntegerField(
        verbose_name="Nombre de participants", default=0)
    user = models.ForeignKey(CustomUser, null=True, blank=True,
                             verbose_name="Gars qui s'inscrit", on_delete=models.CASCADE)
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, null=True, verbose_name="Activité", related_name="inscriptions")
    slug = models.SlugField(max_length=255, null=True,
                            unique=True, verbose_name="Slug")

    class Meta:
        verbose_name = 'inscription'
        verbose_name_plural = 'inscriptions'

    def __str__(self):
        return self.remarks

    def save(self, *args, **kwargs):
        """
        Fonction apelée à la sauvegarde de l'inscription.
        """
        if not self.slug:
            self.slug = generate_unique_vanity(5, 10, Inscription)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("koolapic:inscription", kwargs={'slug': self.slug})


class Donation(models.Model):
    """
    Modèle représentant un don.
    """

    amount = models.FloatField(verbose_name="Montant")
    date = models.DateTimeField(verbose_name="Date de la donation")
    description = models.TextField(
        max_length=500, null=True, blank=True, verbose_name="Description")
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, verbose_name="Utilisateur")
    group = models.ForeignKey(
        Group, on_delete=models.DO_NOTHING, null=True, verbose_name="Groupe")

    def __str__(self):
        return self.description


class Notification(models.Model):
    """
    Modèle représentant une notification.
    """

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

    severity = models.CharField(
        max_length=10, default="INFO", verbose_name="Sévérité")
    title = models.CharField(max_length=100, verbose_name="Titre")
    description = models.CharField(max_length=250, verbose_name="Description")
    link = models.CharField(max_length=250, null=True,
                            blank=True, verbose_name="Lien")
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name='Utilisateur')
    date_sent = models.DateTimeField(
        auto_now_add=True, verbose_name="Date d'envoi")
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Groupe")

    class Meta:
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'

    def __str__(self):
        return self.title


class Invitation(models.Model):
    """
    Modèle représentant une invitation à un groupe.
    """

    ACCEPTATION_CHOICES = [
        ('ACC', 'Acceptée'),
        ('NAC', 'Non acceptée')
    ]

    date = models.DateTimeField(verbose_name="Date d'envoi", auto_now=True)
    slug = models.SlugField(max_length=10, null=True,
                            unique=True, verbose_name="Vanité d'invitation")
    sender = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, related_name="sender",
                               verbose_name="Envoyeur")
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, related_name="receiver",
                             verbose_name="Utilisateur")
    group = models.ForeignKey(
        Group, null=True, on_delete=models.CASCADE, verbose_name="Groupe")

    class Meta:
        verbose_name = 'invitation'
        verbose_name_plural = 'invitations'

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        """
        Fonction apelée à la sauvegarde de l'invitation.
        """
        if not self.slug:
            self.slug = generate_unique_vanity(5, 10, Invitation)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("koolapic:invitation", kwargs={'slug': self.slug})
