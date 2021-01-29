from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.views import PasswordChangeView, LoginView

from koolapic.models import Invitation
from .forms import CustomUserCreationForm, CustomUserChangeForm

from .models import CustomUser


class EditUserProfileView(UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('koolapic:home')
    template_name = 'accounts/edit_profile.html'
    success_message = 'Profil modifié avec succès !'
    context_object_name = 'profile'

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.username
        return context


class UserProfileView(DetailView):
    model = CustomUser
    template_name = 'accounts/profile.html'
    view_as = 'self'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profil'
        context['description'] = 'Voir son profil'
        context['view_as'] = self.view_as
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get("view_as") is None or request.GET.get("view_as") == "" or request.GET.get("view_as") == "self":
            self.view_as = 'self'
        else:
            self.view_as = 'guest'
        return super(UserProfileView, self).get(request, *args, **kwargs)


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('accounts:profile')
    success_message = 'Mot de passe changé avec succès !'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Compte'
        context['description'] = 'Changer le mot de passe du compte'
        return context


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('koolapic:home')
    template_name = 'accounts/signup.html'
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
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        if 'next' in self.request.GET:
            response = redirect(self.request.GET.get('next'))
        return response


class UserLoginView(SuccessMessageMixin, LoginView):
    authentication_form = AuthenticationForm
    template_name = 'accounts/login.html'
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
    template_name = 'accounts/logout.html'

    def post(self, request):
        logout(request)
        messages.success(request, 'Vous avez été déconnecté avec succès !')
        return redirect("koolapic:homepage")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Compte'
        context['description'] = 'Se déconnecter de son compte'
        return context
