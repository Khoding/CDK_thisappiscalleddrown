"""
Fichier contenant les balises de gabarit.
"""

from django import template

register = template.Library()


@register.inclusion_tag('extras/form_extra.html')
def form(form_obj):
    """
    Crée et met en forme un formulaire.

    Arguments nommés :
    form_obj -- objet de formulaire
    """

    return {'form': form_obj}


@register.inclusion_tag('extras/weekday_extra.html')
def weekday(date):
    """
    Retourne le jour de la semaine en fonction d'un datetime.

    Arguments nommés :
    date -- date
    """

    return {'date': date}


@register.inclusion_tag('extras/hour_extra.html')
def hour(date):
    """
    Retourne l'heure au format [hh]h[mm] en fonction d'un datetime.

    Arguments nommés :
    date -- date
    """

    return {'date': date}



@register.inclusion_tag('extras/form_field_extra.html')
def form_field(field):
    """
    Crée un champ de formulaire.

    Arguments nommés :
    dield -- champ de formulaire
    """

    return {
        'field': field,
    }


@register.inclusion_tag('extras/field_label_extra.html')
def field_label(field):
    """
    Crée un label de formulaire.

    Arguments nommés :
    field -- champ de formulaire
    """

    return {
        'field': field,
    }
