from koolapicAPI.models import Notification


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
    return Notification.objects.filter(user=user, status="U").exclude(severity="DEBUG").count()
