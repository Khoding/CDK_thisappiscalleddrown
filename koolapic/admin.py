from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.admin.apps import AdminConfig

from koolapic.models import Activity, Group, Inscription, Invitation, Notification, Donation


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    pass


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    pass
