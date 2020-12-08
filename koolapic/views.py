from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from koolapicAPI.models import Activity, Group

from koolapicAPI.forms import CustomActivityCreationForm, CustomActivityChangeForm, CustomGroupCreationForm, CustomGroupChangeForm


class IndexView(TemplateView):
    template_name = 'koolapic/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Koolapic vous permet de planifier vos activités de groupe avec facilité sur le Web 2.0'
        return context


class ActivityListView(LoginRequiredMixin, ListView):
    template_name = 'koolapic/activities/activity_list.html'
    model = Activity
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Koolapic vous permet de planifier vos activités de groupe avec facilité sur le Web 2.0'
        return context


class ActivityDetailView(LoginRequiredMixin, DetailView):
    model = Activity
    template_name = "koolapic/activities/activity_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Koolapic vous permet de planifier vos activités de groupe avec facilité sur le Web 2.0'
        return context


class ActivityCreateView(LoginRequiredMixin, CreateView):
    template_name = 'koolapic/activities/add_activity.html'
    form_class = CustomActivityCreationForm
    success_url = reverse_lazy("koolapic:activity_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Koolapic vous permet de planifier vos activités de groupe avec facilité sur le Web 2.0'
        return context


class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = Activity
    template_name = 'koolapic/activities/update_activity.html'
    form_class = CustomActivityChangeForm
    success_url = reverse_lazy("koolapic:activity_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Koolapic vous permet de planifier vos activités de groupe avec facilité sur le Web 2.0'
        return context


class ActivityDeleteView(LoginRequiredMixin, DeleteView):
    model = Activity
    template_name = 'koolapic/activities/activity_confirm_delete.html'
    success_url = reverse_lazy("koolapic:activity_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Koolapic vous permet de planifier vos activités de groupe avec facilité sur le Web 2.0'
        return context


class GroupListView(LoginRequiredMixin, ListView):
    template_name = 'koolapic/groups/group_list.html'
    model = Group
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Koolapic vous permet de planifier vos activités de groupe avec facilité sur le Web 2.0'
        return context


class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Group
    template_name = "koolapic/groups/group_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Koolapic vous permet de planifier vos activités de groupe avec facilité sur le Web 2.0'
        return context


class GroupCreateView(LoginRequiredMixin, CreateView):
    template_name = 'koolapic/groups/add_group.html'
    form_class = CustomGroupCreationForm
    success_url = reverse_lazy("koolapic:group_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Koolapic vous permet de planifier vos activités de groupe avec facilité sur le Web 2.0'
        return context


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    template_name = 'koolapic/groups/update_group.html'
    form_class = CustomGroupChangeForm
    success_url = reverse_lazy("koolapic:group_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Koolapic vous permet de planifier vos activités de groupe avec facilité sur le Web 2.0'
        return context


class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = 'koolapic/groups/group_confirm_delete.html'
    success_url = reverse_lazy("koolapic:group_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Koolapic vous permet de planifier vos activités de groupe avec facilité sur le Web 2.0'
        return context
