"""
Fichier relatif aux processeurs de contexte.
"""

import datetime

from utils.notifications import get_all_unread_notifications_number


def get_current_year_to_context(request):
    """
    Ajoute l'année actuelle au contexte.

    Arguments nommés :
    request -- requête
    """

    current_datetime = datetime.datetime.now()
    return {
        'current_year': current_datetime.year
    }


def get_unread_notifications_number_to_context(request):
    """
    Ajoute le nombre de notifications non lues au contexte.

    Arguments nommés :
    request -- requête
    """

    number = 0
    if request.user.is_authenticated:
        number = get_all_unread_notifications_number(request.user)
    return {
        'unread_notifications_number': number
    }
