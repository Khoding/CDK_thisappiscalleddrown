from django.contrib import admin
from koolapicAPI.models import Activity, Group, Inscription, Admission, Notification, Donation


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


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    pass


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    pass
