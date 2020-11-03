from django import template

register = template.Library()
from ..models import CustomUser


@register.simple_tag
def all_user_objects():
    return CustomUser.address
