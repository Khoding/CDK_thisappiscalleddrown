from django import template
from ..models import CustomUser

register = template.Library()


@register.simple_tag
def all_user_objects():
    return CustomUser.address
