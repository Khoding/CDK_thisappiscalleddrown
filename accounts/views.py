"""
Vues de l'application Accounts.
"""

import json

from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView, TemplateView, CreateView

from koolapic.models import Invitation
from .forms import EditProfileForm, CustomUserCreationForm
from .models import CustomUser


class EditUserProfileView(UpdateView):
    """
    Vue d'édition du profil d'utilisateur.
    """

    form_class = EditProfileForm
    success_url = reverse_lazy('koolapic:home')
    template_name = 'account/edit_profile.html'
    success_message = 'Profil modifié avec succès !'
    context_object_name = 'profile'

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"{self.object.first_name} {self.object.last_name}"
        return context


class UserProfileView(DetailView):
    """
    Vue de détail du profil d'utilisateur.
    """

    model = CustomUser
    template_name = 'account/profile/profile.html'
    view_as = 'self'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profil'
        context['description'] = 'Voir son profil'
        context['view_as'] = self.view_as
        context['invitations'] = Invitation.objects.filter(sender=self.request.user)
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get("view_as") is None or request.GET.get("view_as") == "" or request.GET.get(
                "view_as") == "self":
            self.view_as = 'self'
        else:
            self.view_as = 'guest'
        return super(UserProfileView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'disconnectUser' in self.request.POST:
            logout(request)
            messages.success(request, 'Vous avez été déconnecté avec succès !')
            return redirect("koolapic:homepage")
        elif self.request.body:
            data = json.loads(self.request.body.decode('utf-8'))
            if data['action'] == 'deleteInvitation':
                invitation = Invitation.objects.get(slug=data['invitationSlug'])
                invitation.delete()
                return HttpResponse(status=200)


class PasswordsChangeView(PasswordChangeView):
    """
    Vue de changement de mot de passe utilisateur.
    """

    form_class = PasswordChangeForm
    template_name = 'account/change_password.html'
    success_url = reverse_lazy('accounts:profile')
    success_message = 'Mot de passe changé avec succès !'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Compte'
        context['description'] = 'Changer le mot de passe du compte'
        return context


class SignupView(CreateView):
    """
    Vue de création de compte utilisateur.
    """

    form_class = CustomUserCreationForm
    success_url = reverse_lazy('koolapic:home')
    template_name = 'account/signup.html'
    success_message = 'Compte créé avec succès !'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Compte'
        context['description'] = 'Créer un compte sur Koolapic.'
        if 'next' in self.request.GET:
            context['next'] = self.request.GET.get('next')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        user = authenticate(
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        if 'next' in self.request.GET:
            response = redirect(self.request.GET.get('next'))
        return response


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Vue de connexion à un utilisateur.
    """

    authentication_form = AuthenticationForm
    template_name = 'account/login.html'
    success_message = "Vous avez été connecté avec succès !"
    success_url = reverse_lazy('koolapic:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'invitation' in self.request.session:
            invitation_slug = self.request.session['invitation']
            invitation = Invitation.objects.get(slug=invitation_slug)
            context['invitation'] = invitation
            context['members_count'] = invitation.group.members.count() + invitation.group.admins.count()
            # del self.request.session['invitation']
        if 'next' in self.request.GET:
            context['next'] = self.request.GET.get('next')

        context['title'] = 'Compte'
        context['description'] = 'Se connecter à son compte sur Koolapic.'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if 'next' in self.request.GET:
            redirect(self.request.GET.get('next'))
        return response


class UserLogoutView(TemplateView):
    template_name = 'account/logout.html'

    def post(self, request):
        logout(request)
        messages.success(request, 'Vous avez été déconnecté avec succès !')
        return redirect("koolapic:homepage")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Compte'
        context['description'] = 'Se déconnecter de son compte'
        return context
