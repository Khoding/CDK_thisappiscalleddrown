import datetime

from utils.notifications import get_unread_notifications_number


def get_current_year_to_context(request):
    current_datetime = datetime.datetime.now()
    return {
        'current_year': current_datetime.year
    }


def get_unread_notifications_number_to_context(request):
    number = 0
    if request.user.is_authenticated:
        number = get_unread_notifications_number(request.user)
    return {
        'unread_notifications_number': number
    }
