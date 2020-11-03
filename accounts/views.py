from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView

from .forms import CustomUserCreationForm, CustomUserChangeForm

from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'account/signup.html'


class UserEditView(UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('home')
    template_name = 'account/edit_profile.html'

    def get_object(self, queryset=True):
        return self.request.user


class UserProfileView(DetailView):
    model = CustomUser
    template_name = 'account/profile.html'

    def get_object(self, queryset=True):
        return self.request.user


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'account/change_password.html'
    success_url = reverse_lazy('profile')
