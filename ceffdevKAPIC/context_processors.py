import datetime

from koolapicAPI.models import Notification
from utils.notifications import get_unread_notifications_number


def get_current_year_to_context(request):
    current_datetime = datetime.datetime.now()
    return {
        'current_year': current_datetime.year
    }


def get_unread_notifications_number_to_context(request):
    return {
        'unread_notifications_number': get_unread_notifications_number(request.user)
    }
