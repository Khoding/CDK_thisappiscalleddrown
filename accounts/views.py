from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.views import PasswordChangeView, LoginView

from .forms import CustomUserCreationForm, CustomUserChangeForm

from .models import CustomUser


class EditUserProfileView(UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('koolapic:home')
    template_name = 'accounts/edit_profile.html'

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.username
        return context


class UserProfileView(DetailView):
    model = CustomUser
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profil'
        context['description'] = 'Voir son profil'
        return context


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('accounts:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Compte'
        context['description'] = 'Changer le mot de passe du compte'
        return context


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'
    success_message = 'Compte créé avec succès'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Compte'
        context['description'] = 'Créer un compte'
        return context


class UserLoginView(LoginView):
    authentication_form = AuthenticationForm
    redirect_field_name = reverse_lazy('koolapic:home')
    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Compte'
        context['description'] = 'Se connecter à son compte'
        return context


class UserLogoutView(TemplateView):
    authentication_form = AuthenticationForm
    redirect_field_name = reverse_lazy('koolapic:home')
    template_name = 'accounts/logout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Compte'
        context['description'] = 'Se déconnecter de son compte'
        return context
