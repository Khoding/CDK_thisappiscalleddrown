from koolapic.models import Notification, Invitation


def send_notification(user, title, severity, description, **kwargs):
    link = kwargs.get("link", "")

    notification = Notification(user=user, title=title, severity=severity, description=description, link=link)
    notification.save()


def send_group_notification(user, title, severity, description, group, **kwargs):
    link = kwargs.get("link", "")

    notification = Notification(user=user, title=title, severity=severity, description=description, group=group, link=link)
    notification.save()


def hide_notification(notification):
    notification.status = "D"
    notification.save()


def get_unread_notifications_number(user):
    return Notification.objects.filter(user=user).exclude(severity="DEBUG").count()


def get_group_invitations_number(user):
    return Invitation.objects.filter(user=user).count()


def get_all_unread_notifications_number(user):
    return get_unread_notifications_number(user=user) + get_group_invitations_number(user=user)


def notifications_to_dictionary(user):
    return {
        'all_unread_notifications_number': get_all_unread_notifications_number(user=user),
        'unread_notifications_number': get_all_unread_notifications_number(user=user),
        'group_invitations_number': get_all_unread_notifications_number(user=user),
    }
