from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView
from django.contrib import messages
from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser


class IndexView(TemplateView):
    template_name = 'koolapic/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Koolapic vous permet de planifier vos activités de groupe avec facilité sur le Web 2.0'
        return context


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'koolapic/signup.html'
    success_message = 'Compte créé avec succès'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Compte Koolapic'
        context['description'] = 'Créer un compte sur Koolapic'
        return context


class KoolapicLoginView(LoginView):
    authentication_form = AuthenticationForm
    redirect_field_name = reverse_lazy('index')
    template_name = 'koolapic/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Compte Koolapic'
        context['description'] = 'Se connecter à son compte sur Koolapic'
        return context


class LogoutView(TemplateView):
    pass
