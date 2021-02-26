"""
Fichier relatif à l'administration de l'application Accounts.
"""

from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    """
    Modèle d'administration pour la classe CustomUser.
    """

    list_display = ['email', 'slug']


admin.site.register(CustomUser, CustomUserAdmin)
