from accounts.models import CustomUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.aggregates import Sum
from django.urls import reverse, reverse_lazy
from utils.db_utils import generate_unique_vanity
from model_utils import FieldTracker


class Group(models.Model):
    """
    Modèle représentant un groupe Koolapic.
    """

    name = models.CharField(max_length=50, verbose_name="Nom du groupe")
    description = models.TextField(max_length=200, verbose_name="Description")
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to="images/groups/",
        verbose_name="Image du groupe",
    )
    banner_color = models.CharField(max_length=8, verbose_name="Couleur de la bannière")
    slug = models.SlugField(null=True, unique=True, verbose_name="Slug")

    members = models.ManyToManyField(
        CustomUser,
        related_name="members",
        related_query_name="member",
        verbose_name="Utilisateurs",
    )
    admins = models.ManyToManyField(
        CustomUser,
        related_name="admins",
        related_query_name="admin",
        verbose_name="Administrateurs du groupe",
    )

    website = models.TextField(max_length=100, null=True, blank=True, verbose_name="Site web")

    class Meta:
        verbose_name = "groupe"
        verbose_name_plural = "groupes"

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
        return reverse("koolapic:group_detail", kwargs={"slug": self.slug})

    def get_add_url(self):
        return reverse("koolapic:add_group", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse("koolapic:update_group", kwargs={"slug": self.slug})

    def get_confirm_delete_url(self):
        return reverse("koolapic:group_confirm_delete", kwargs={"slug": self.slug})


class Activity(models.Model):
    """
    Modèle représentant une activité.
    """

    name = models.CharField(max_length=32, default="Activité sans nom", verbose_name="Nom de l'activité")
    description = models.TextField(max_length=500, verbose_name="Description")
    creator = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        verbose_name="Créateur",
        on_delete=models.CASCADE,
    )

    remarks = models.TextField(max_length=500, null=True, blank=True, verbose_name="Remarques")
    max_participants = models.PositiveIntegerField(null=True, blank=True, verbose_name="Max de participants")

    start_location = models.CharField(max_length=100, null=True, verbose_name="Lieu de départ")
    start_date = models.DateTimeField(verbose_name="Date de début")

    end_location = models.CharField(max_length=100, null=True, blank=True, verbose_name="Lieu de fin")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Date de fin")

    last_update = models.DateTimeField(verbose_name="Dernière mise à jour", auto_now=True)
    participants = models.ManyToManyField(
        CustomUser,
        related_name="participants",
        related_query_name="participant",
        verbose_name="Participants",
        blank=True,
    )
    slug = models.SlugField(max_length=255, null=True, unique=True, verbose_name="Slug")
    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE, verbose_name="Groupe")

    class Meta:
        verbose_name = "activité"
        verbose_name_plural = "activités"
        # constraints = [
        #     CheckConstraint(
        #         check=Q(property.total__gte=F("max_participants")),
        #         name="check_max",
        #     ),
        # ]

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
        return reverse("koolapic:activity_detail", kwargs={"slug": self.slug})

    def get_clone_old_url(self):
        return reverse("koolapic:clone_activity", kwargs={"slug": self.slug})

    def get_clone_url(self):
        return reverse("koolapic:clone_activity_ajax", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse("koolapic:update_activity", kwargs={"slug": self.slug})

    def get_confirm_delete_url(self):
        return reverse("koolapic:activity_confirm_delete", kwargs={"slug": self.slug})

    @property
    def total(self):
        guests = (
            self.participants.filter(inscription__presence=True)
            .aggregate(Sum("inscription__guests_number"))
            .get("inscription__guests_number__sum")
        )
        users = self.inscriptions.filter(presence=True).count()
        return guests + users


class Inscription(models.Model):
    """
    Modèle représentant une inscription à une activité.
    """

    date = models.DateTimeField(verbose_name="Date de l'inscription", auto_now=True)
    remarks = models.TextField(max_length=500, blank=True, default="", verbose_name="Remarques")
    presence = models.BooleanField(verbose_name="Présence", default=True)
    guests_number = models.PositiveIntegerField(verbose_name="Accompagnants", default=0)
    user = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        verbose_name="Gars qui s'inscrit",
        on_delete=models.CASCADE,
    )
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Activité",
        related_name="inscriptions",
    )
    slug = models.SlugField(max_length=255, null=True, unique=True, verbose_name="Slug")
    tracker_guests = FieldTracker(fields=["guests_number"])
    tracker_presence = FieldTracker(fields=["presence"])

    class Meta:
        verbose_name = "inscription"
        verbose_name_plural = "inscriptions"

    def __str__(self):
        return f"{self.activity} - {self.user}"

    # def clean(self):
    #     if self.total > self.activity.max_participants:
    #         raise ValidationError("lol")
    #     return super().clean()

    def get_totalnum(self):
        guests = (
            self.activity.participants.filter(inscription__presence=True)
            .aggregate(Sum("inscription__guests_number"))
            .get("inscription__guests_number__sum")
        )
        users = self.activity.inscriptions.filter(presence=True).count()
        total = guests + users
        return total

    def save(self, *args, **kwargs):
        """
        Fonction apelée à la sauvegarde de l'inscription.
        """
        if not self.slug:
            self.slug = generate_unique_vanity(5, 10, Inscription)

        if self.activity.max_participants:
            if self.get_totalnum() > self.activity.max_participants:
                raise ValidationError("x")
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("koolapic:inscription", kwargs={"slug": self.slug})

    @property
    def total(self):
        guests = (
            self.activity.participants.filter(inscription__presence=True)
            .aggregate(Sum("inscription__guests_number"))
            .get("inscription__guests_number__sum")
        )
        users = self.activity.inscriptions.filter(presence=True).count()
        return guests + users


class Donation(models.Model):
    """
    Modèle représentant un don.
    """

    amount = models.FloatField(verbose_name="Montant")
    date = models.DateTimeField(verbose_name="Date de la donation")
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name="Description")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, verbose_name="Utilisateur")
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True, verbose_name="Groupe")

    def __str__(self):
        return self.description


class Notification(models.Model):
    """
    Modèle représentant une notification.
    """

    SEVERITY_CHOICES = [
        ("DEBUG", "Débogage"),
        ("INFO", "Information"),
        ("WARNING", "Avertissement"),
        ("DANGER", "Danger"),
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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Utilisateur")
    date_sent = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Groupe")

    class Meta:
        verbose_name = "notification"
        verbose_name_plural = "notifications"

    def __str__(self):
        return self.title


class Invitation(models.Model):
    """
    Modèle représentant une invitation à un groupe.
    """

    ACCEPTATION_CHOICES = [("ACC", "Acceptée"), ("NAC", "Non acceptée")]

    date = models.DateTimeField(verbose_name="Date d'envoi", auto_now=True)
    slug = models.SlugField(max_length=10, null=True, unique=True, verbose_name="Vanité d'invitation")
    sender = models.ForeignKey(
        CustomUser,
        null=True,
        on_delete=models.CASCADE,
        related_name="sender",
        verbose_name="Envoyeur",
    )
    user = models.ForeignKey(
        CustomUser,
        null=True,
        on_delete=models.CASCADE,
        related_name="receiver",
        verbose_name="Utilisateur",
    )
    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE, verbose_name="Groupe")

    class Meta:
        verbose_name = "invitation"
        verbose_name_plural = "invitations"

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
        return reverse_lazy("koolapic:invitation", kwargs={"slug": self.slug})
