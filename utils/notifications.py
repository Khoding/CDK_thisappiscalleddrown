"""
Fichier contenant des fonctions utilitaires pour la gestion des notifications.
"""

from thisappiscalleddrown.models import Notification, Invitation

SEVERITY_DANGER = "DANGER"
SEVERITY_WARNING = "WARNING"
SEVERITY_SUCCESS = "SUCCESS"
SEVERITY_DEBUG = "DEBUG"


def send_notification(user, title, severity, description, **kwargs):
    """
    Envoie une notification à un utilisateur.

    Arguments nommés :
    user -- utilisateur
    title -- titre de la notification
    severity -- sévérité de la notification
    description -- description de la notification

    Kwargs :
    link -- lien de redirection de la notification
    """

    link = kwargs.get("link", "")

    notification = Notification(user=user, title=title, severity=severity, description=description, link=link)
    notification.save()


def send_group_notification(user, title, severity, description, group, **kwargs):
    """
    Envoie une notification de groupe à un utilisateur.

    Arguments nommés :
    user -- utilisateur
    title -- titre de la notification
    severity -- sévérité de la notification
    description -- description de la notification
    group -- groupe de la notification

    Kwargs :
    link -- lien de redirection de la notification
    """

    link = kwargs.get("link", "")

    notification = Notification(user=user, title=title, severity=severity, description=description, group=group,
                                link=link)
    notification.save()


def get_unread_notifications_number(user):
    """
    Retourne le nombre de notifications non lues d'un utilisateur.

    Arguments nommés :
    user -- utilisateur
    """

    return Notification.objects.filter(user=user).exclude(severity="DEBUG").count()


def get_group_invitations_number(user):
    """
    Retourne le nombre de notifications de groupe non lues d'un utilisateur.

    Arguments nommés :
    user -- utilisateur
    """

    return Invitation.objects.filter(user=user).count()


def get_all_unread_notifications_number(user):
    """
    Retourne le nombre de notifications non lues totales d'un utilisateur.

    Arguments nommés :
    user (accounts.CustomUser) -- utilisateur
    """

    return get_unread_notifications_number(user=user) + get_group_invitations_number(user=user)


def unread_notifications_number_to_dictionary(user):
    """
    Retourne un dictionnaire contenant le nombre de tous les types de notifications non lues.

    Arguments nommés :
    user -- utilisateur
    """

    return {
        'all_unread_notifications_number': get_all_unread_notifications_number(user=user),
        'unread_notifications_number': get_all_unread_notifications_number(user=user),
        'group_invitations_number': get_all_unread_notifications_number(user=user),
    }
