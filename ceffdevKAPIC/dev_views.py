from django.views.generic import TemplateView


class Error400View(TemplateView):
    template_name = '400.html'


class Error404View(TemplateView):
    template_name = '404.html'


class Error403View(TemplateView):
    template_name = '403.html'


class Error500View(TemplateView):
    template_name = '500.html'
