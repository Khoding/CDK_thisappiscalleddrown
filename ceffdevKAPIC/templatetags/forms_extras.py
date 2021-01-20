from django import template

register = template.Library()


@register.inclusion_tag('extras/form_extra.html')
def form(form_obj):
    return {'form': form_obj}
