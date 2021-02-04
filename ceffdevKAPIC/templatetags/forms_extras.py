from django import template

register = template.Library()


@register.inclusion_tag('extras/form_extra.html')
def form(form_obj):
    return {'form': form_obj}


@register.inclusion_tag('extras/map_input_extra.html')
def map_input(address, width, height, zoom):
    return {
        'form': address,
        'width': width,
        'height': height,
        'zoom': zoom
    }
