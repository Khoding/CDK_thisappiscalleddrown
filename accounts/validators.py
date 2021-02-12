from django.core.exceptions import ValidationError

from accounts.models import CustomUser


def validate_user_email(value):
    if CustomUser.objects.filter(email=value).exists():
        raise ValidationError("Cette adresse e-mail est déjà utilisée.")
