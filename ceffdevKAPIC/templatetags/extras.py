from django import template

register = template.Library()


@register.inclusion_tag('extras/form_extra.html')
def form(form_obj):
    return {'form': form_obj}


@register.inclusion_tag('extras/weekday_extra.html')
def weekday(date):
    return {'date': date}


@register.inclusion_tag('extras/hour_extra.html')
def hour(date):
    return {'date': date}


@register.inclusion_tag('extras/spoiler_extra.html')
def spoiler(field):
    return {
        'field': field,
    }


@register.inclusion_tag('extras/form_field_extra.html')
def form_field(field):
    return {
        'field': field,
    }

@register.inclusion_tag('extras/field_label_extra.html')
def field_label(field):
    return {
        'field': field,
    }

@register.inclusion_tag('extras/map_input_extra.html')
def map_input(address, width, height, zoom):
    return {
        'form': address,
        'width': width,
        'height': height,
        'zoom': zoom
    }
