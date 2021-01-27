import json

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser
from koolapic.models import Activity, Group, Invitation, Notification

from koolapic.forms import CustomActivityCreationForm, CustomActivityChangeForm, CustomGroupCreationForm, CustomGroupChangeForm, InvitationCreationForm
from utils.notifications import notifications_to_dictionary


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'koolapic/index.html'

    def get_activities(self):
        if self.request.user.is_superuser:
            return Activity.objects.all
        else:
            return Activity.objects.order_by('start_date').filter(participants=self.request.user)

    def get_groups(self):
        if self.request.user.is_superuser:
            return Group.objects.all().annotate(members_count=Count('members'))
        else:
            return Group.objects.order_by('name').annotate(members_count=Count('members')).filter(members=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Koolapic vous permet de planifier vos activités de groupe avec facilité sur le Web 2.0'
        context['activities'] = self.get_activities()
        context['groups'] = self.get_groups()
        return context


class NotificationsView(LoginRequiredMixin, TemplateView):
    template_name = 'koolapic/notifications/notifications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['notifications'] = Notification.objects.filter(user=self.request.user).order_by('-date_sent')
        context['invitations'] = Invitation.objects.filter(user=self.request.user).order_by('-date')
        context['description'] = 'Koolapic vous permet de planifier vos activités de groupe avec facilité sur le Web 2.0'
        return context

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        if data['action'] == 'deleteNotification':
            notification_id = data['notification']
            notification = Notification.objects.get(id=notification_id)
            notification.delete()
            response_data = notifications_to_dictionary(user=self.request.user)
            return JsonResponse(response_data)

        if data['action'] == "deleteAllNotifications":
            Notification.objects.filter(user=self.request.user).delete()
            return HttpResponse(status=200)


class HomeView(TemplateView):
    template_name = 'koolapic/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Koolapic vous permet de planifier vos activités de groupe avec facilité sur le Web 2.0'
        return context


class ActivityListView(LoginRequiredMixin, ListView):
    template_name = 'koolapic/activities/activity_list.html'
    context_object_name = 'activities'
    model = Activity

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all
        else:
            return self.model.objects.order_by('start_date').filter(participant=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'La liste des activités sur Koolapic'
        return context


class ActivityDetailView(LoginRequiredMixin, DetailView):
    model = Activity
    template_name = "koolapic/activities/activity_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'La page détail d\'une activités sur Koolapic'
        return context


class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = Activity
    template_name = 'koolapic/activities/add_activity.html'
    form_class = CustomActivityCreationForm
    success_url = reverse_lazy("koolapic:activity_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Créer une activité sur Koolapic'
        return context


class ActivityCloneView(LoginRequiredMixin, CreateView):
    model = Activity
    template_name = 'koolapic/activities/add_activity.html'
    form_class = CustomActivityCreationForm
    success_url = reverse_lazy("koolapic:activity_list")

    def get_context_data(self, **kwargs):
        activity = self.get_object()

        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Créer une activité sur Koolapic'
        context['form'] = CustomActivityCreationForm(instance=activity)
        return context


class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = Activity
    template_name = 'koolapic/activities/update_activity.html'
    form_class = CustomActivityChangeForm
    success_url = reverse_lazy("koolapic:activity_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Modifier une activité sur Koolapic'
        return context


class ActivityDeleteView(LoginRequiredMixin, DeleteView):
    model = Activity
    template_name = 'koolapic/activities/activity_confirm_delete.html'
    success_url = reverse_lazy("koolapic:activity_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Supprime une activité sur Koolapic'
        return context


class GroupListView(LoginRequiredMixin, ListView):
    template_name = 'koolapic/groups/group_list.html'
    model = Group
    context_object_name = 'groups'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all().annotate(members_count=Count('members'))
        else:
            return self.model.objects.order_by('name').annotate(members_count=Count('members')).filter(members=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'La liste des groupes sur Koolapic'
        return context


class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Group
    template_name = 'koolapic/groups/group_detail.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        admins = self.object.admins.all()
        admin_ids = admins.values_list('id', flat=True)
        members = self.object.members.all().exclude(id__in=admin_ids)
        banned_users = self.object.banned_users.all()
        all_members_count = len(members) + len(admins)

        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'La page détail d\'un groupe sur Koolapic'
        context['members'] = members
        context['admins'] = admins
        context['banned_users'] = banned_users
        context['all_members'] = members | admins
        context['members_count'] = all_members_count
        context['undisplayed_members_count'] = all_members_count - 10
        context['invitation_form'] = InvitationCreationForm
        return context

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        if data['action'] == 'join':
            self.get_object().members.add(self.request.user)
            return HttpResponse(status=200)
        elif data['action'] == 'leave':
            self.get_object().members.remove(self.request.user)
            return HttpResponse(status=200)
        elif data['action'] == 'invite':
            form = InvitationCreationForm(data['form'])

            if form.is_valid():
                if CustomUser.objects.filter(email=form.cleaned_data.get("email")).count() > 0:
                    user = CustomUser.objects.get(email=form.cleaned_data.get("email"))
                    message = form.cleaned_data.get("message")
                    group = self.get_object()

                    if user in group.members.all() or user in group.admins.all():
                        message = {
                            "text": "Cet utilisateur appartient déjà ce groupe.",
                            "severity": "ERROR"
                        }
                    elif user in group.banned_users.all():
                        message = {
                            "text": "Cet utilisateur est banni de ce groupe.",
                            "severity": "ERROR"
                        }
                    else:
                        if Invitation.objects.filter(user=user, group=group).count() == 0:
                            invitation = Invitation(user=user, sender=self.request.user, group=group, message=message)
                            invitation.save()
                            message = {
                                "text": "Invitation envoyée.",
                                "severity": "SUCCESS"
                            }
                        else:
                            message = {
                                "text": "Cet utilisateur a déjà été invité à ce groupe.",
                                "severity": "ERROR"
                            }

                else:
                    # TODO invitation quand le user n'a pas de compte
                    message = {
                        "text": "La personne n'a pas de compte Koolapic.",
                        "severity": "WARNING"
                    }
                response_data = {
                    'message': message,
                }
                return JsonResponse(response_data)
            else:
                message = {
                    "text": "Les champs du formulaires ne sont pas valides.",
                    "severity": "ERROR"
                }
                response_data = {
                    'message': message
                }
                return JsonResponse(response_data)


class InvitationView(LoginRequiredMixin, DetailView):
    template_name = 'koolapic/groups/invitation.html'
    model = Invitation
    context_object_name = 'invitation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = f'Invitation au groupe {self.object.group}'
        return context

    def post(self, *args, **kwargs):
        group = self.get_object().group
        if self.request.user == self.get_object().user:
            if self.request.POST.get('accept'):
                self.get_object().group.members.add(self.get_object().user)
                self.model.objects.get(id=self.get_object().id).delete()
                messages.success(request=self.request, message=f"Vous faites désormais partie du groupe {group.name}.")
                return redirect(reverse('koolapic:group_detail', kwargs={'slug': group.slug}))
            elif self.request.POST.get('decline'):
                messages.success(request=self.request, message=f"Vous avez décliné l'invitation au groupe {group.name}.")
                self.model.objects.get(id=self.get_object().id).delete()
                return redirect(reverse('koolapic:home'))
        else:
            messages.error(request=self.request, message="Cette invitation ne vous est pas destinée.")
            return redirect(reverse('koolapic:home'))


class GroupCreateView(LoginRequiredMixin, CreateView):
    template_name = 'koolapic/groups/add_group.html'
    form_class = CustomGroupCreationForm
    success_url = reverse_lazy("koolapic:group_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Créer un groupe sur Koolapic'
        return context


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    template_name = 'koolapic/groups/update_group.html'
    form_class = CustomGroupChangeForm
    success_url = reverse_lazy("koolapic:group_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Modifie un groupe sur Koolapic'
        return context


class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = 'koolapic/groups/group_confirm_delete.html'
    success_url = reverse_lazy("koolapic:group_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Supprime un groupe sur Koolapic'
        return context


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'account/signup.html'
    success_message = 'Compte créé avec succès'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Compte Koolapic'
        context['description'] = 'Créer un compte sur Koolapic'
        return context


class KoolapicLoginView(LoginView):
    authentication_form = AuthenticationForm
    redirect_field_name = reverse_lazy('koolapic:index')
    template_name = 'account/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Compte Koolapic'
        context['description'] = 'Se connecter à son compte sur Koolapic'
        return context


class ConditionsView(TemplateView):
    pass


class ConfidentialityView(TemplateView):
    pass


class LicenseView(TemplateView):
    pass
