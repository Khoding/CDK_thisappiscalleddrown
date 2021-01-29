import json

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser
from ceffdevKAPIC.custom_settings import MAX_INVITATION_NUMBER_BY_USER
from koolapic.models import Activity, Group, Invitation, Notification, generate_unique_vanity

from koolapic.forms import CustomActivityCreationForm, CustomActivityChangeForm, CustomGroupCreationForm, CustomGroupChangeForm, InvitationCreationForm
from utils.notifications import notifications_to_dictionary


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'koolapic/index.html'

    def get(self, *args, **kwargs):
        if 'next' in self.request.GET:
            next_page = self.request.GET.get('next')
            return redirect(next_page)
        return super().get(*args, **kwargs)

    def get_upcoming_activities(self):
        return Activity.objects.order_by('start_date').all().filter(end_date__gte=timezone.now()) if self.request.user.is_superuser \
            else Activity.objects.order_by('start_date').filter(participants=self.request.user).filter(end_date__gte=timezone.now())

    def get_groups(self):
        if self.request.user.is_superuser:
            return Group.objects.all().annotate(members_count=Count('members'))
        else:
            return Group.objects.order_by('name').annotate(members_count=Count('members') + Count('admins')).filter(members=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'Koolapic vous permet de planifier vos activités de groupe avec facilité sur le Web 2.0'
        context['upcoming_activities'] = self.get_upcoming_activities()
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

    def get_activities(self):
        return self.model.objects.order_by('start_date').all() if self.request.user.is_superuser \
            else self.model.objects.order_by('start_date').filter(participants=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = 'La liste des activités sur Koolapic'
        context['upcoming_activities'] = self.get_activities().filter(end_date__gte=timezone.now())
        context['past_activities'] = self.get_activities().filter(end_date__lt=timezone.now())
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
            return self.model.objects.order_by('name').all().annotate(members_count=Count('members'))
        else:
            return self.model.objects.order_by('name').annotate(members_count=Count('members')).filter(Q(admins=self.request.user) |
                                                                                                       Q(members=self.request.user))

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
        elif data['action'] == 'getInvitationLink':
            if Invitation.objects.filter(sender=self.request.user).count() <= MAX_INVITATION_NUMBER_BY_USER:
                invitation = Invitation(sender=self.request.user, group=self.get_object(), slug=generate_unique_vanity(5, 15, Invitation))
                invitation.save()
                return JsonResponse({
                    'invitationLink': invitation.get_absolute_url()
                })
            else:
                response_data = {
                    'message': {
                        "text": "Vous avez atteint la limite du nombre d'invitation par utilisateur. Veuillez réessayer plus tard.",
                        "severity": "ERROR"
                    },
                }
                return JsonResponse(response_data)
        elif data['action'] == 'invite':
            form = InvitationCreationForm(data['form'])

            if form.is_valid():
                if CustomUser.objects.filter(email=form.cleaned_data.get("email")).count() > 0:
                    user = CustomUser.objects.get(email=form.cleaned_data.get("email"))
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
                        if Invitation.objects.filter(sender=self.request.user).count() <= MAX_INVITATION_NUMBER_BY_USER:
                            if Invitation.objects.filter(user=user, group=group).count() == 0:
                                invitation = Invitation(user=user, sender=self.request.user, group=group)
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
                            message = {
                                "text": "Vous avez atteint la limite du nombre d'invitation par utilisateur. Veuillez réessayer plus tard.",
                                "severity": "ERROR"
                            }

                else:
                    message = {
                        "text": "La personne n'a pas de compte Koolapic. Vous pouvez lui envoyer un lien d'invitation.",
                        "severity": "ERROR"
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


class InvitationView(DetailView):
    template_name = 'koolapic/groups/invitation.html'
    model = Invitation
    context_object_name = 'invitation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Koolapic'
        context['description'] = f'Invitation au groupe {self.get_object().group}'
        return context

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            self.request.session['invitation'] = self.get_object().slug
            return redirect(f"{reverse('accounts:login')}?next={self.get_object().get_absolute_url()}")

        if self.request.user in self.get_object().group.members.filter(member__id=self.request.user.id) != 0:
            messages.error(request=self.request, message="Vous faites déjà partie de ce groupe.")
            return redirect(reverse('koolapic:home'))

        if self.request.user in self.get_object().group.banned_users.filter(member__id=self.request.user.id) != 0:
            messages.error(request=self.request, message="Vous avez été banni(e) de ce groupe.")
            return redirect(reverse('koolapic:home'))

        if self.get_object().user and self.request.user != self.get_object().user:
            messages.error(request=self.request, message="Cette invitation ne vous est pas destinée.")
            return redirect(reverse('koolapic:home'))

        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        group = self.get_object().group
        if not self.get_object().user or self.request.user == self.get_object().user:
            if self.request.POST.get('accept'):
                self.get_object().group.members.add(self.request.user)
                if self.get_object().user:
                    self.model.objects.get(id=self.get_object().id).delete()
                messages.success(request=self.request, message=f"Vous faites désormais partie du groupe {group.name}.")
                return redirect(reverse('koolapic:group_detail', kwargs={'slug': group.slug}))
            elif self.request.POST.get('decline'):
                messages.success(request=self.request, message=f"Vous avez décliné l'invitation au groupe {group.name}.")
                if self.get_object().user:
                    self.model.objects.get(id=self.request.user.id).delete()
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

    def form_valid(self, form):
        self.object = form.save()
        self.object.admins.add(self.request.user)
        return redirect(self.get_success_url())


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
    template_name = 'koolapic/licenses.html'
