from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from .forms import CustomUserCreationForm, UserChangeForm, CustomUserChangeForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class UserEditView(UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('home')
    template_name = 'registration/edit_profile.html'

    def get_object(self, queryset=True):
        return self.request.user
