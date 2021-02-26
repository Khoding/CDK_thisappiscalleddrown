"""
Validateurs.
"""

from django.core.exceptions import ValidationError

from accounts.models import CustomUser


def validate_user_email(value):
    """
    Valide l'email d'un utilisateur.

    Arguments nommés :
    value -- valeur
    """

    if CustomUser.objects.filter(email=value).exists():
        raise ValidationError("Cette adresse e-mail est déjà utilisée.")
