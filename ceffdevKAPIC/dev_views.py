"""
Vues utilisées uniquement en développement.
"""

from django.views.generic import TemplateView


class Error400View(TemplateView):
    """
    Vue de test de la page d'erreur 400.
    """

    template_name = '400.html'


class Error404View(TemplateView):
    """
    Vue de test de la page d'erreur 404.
    """

    template_name = '404.html'


class Error403View(TemplateView):
    """
    Vue de test de la page d'erreur 403.
    """

    template_name = '403.html'


class Error500View(TemplateView):
    """
    Vue de test de la page d'erreur 500.
    """

    template_name = '500.html'
