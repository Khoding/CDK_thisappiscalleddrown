"""
Fichier relatif à l'administration de l'application thisappiscalleddrown.
"""

from django.contrib import admin

from thisappiscalleddrown.models import (
    Activity,
    Donation,
    Group,
    Inscription,
    Invitation,
    Notification,
)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """
    Modèle d'administration de la classe Activity.
    """

    prepopulated_fields = {"slug": ("name",)}


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """
    Modèle d'administration de la classe Group.
    """

    prepopulated_fields = {"slug": ("name",)}


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Modèle d'administration de la classe Notification.
    """

    pass


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    """
    Modèle d'administration de la classe Inscription.
    """

    pass


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    """
    Modèle d'administration de la classe Invitation.
    """

    pass


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    """
    Modèle d'administration de la classe Donation.
    """

    pass
