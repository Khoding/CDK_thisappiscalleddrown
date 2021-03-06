import datetime
import json

from accounts.models import CustomUser
from CDK_thisappiscalleddrown.thisappiscalleddrown_settings import CONTRIBUTORS, MAX_INVITATION_NUMBER_BY_USER
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q, Sum
from django.http import HttpResponse, JsonResponse, request
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from utils.notifications import unread_notifications_number_to_dictionary

from thisappiscalleddrown.forms import (
    ActivityChangeForm,
    ActivityCloneForm,
    ActivityCreationForm,
    CustomGroupChangeForm,
    CustomGroupCreationForm,
    InscriptionCreationForm,
    InvitationCreationForm,
)
from thisappiscalleddrown.models import Activity, Group, Inscription, Invitation, Notification


class IndexView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = "thisappiscalleddrown/index.html"
    form_class = InscriptionCreationForm
    context_object_name = "upcoming_activities"
    success_url = reverse_lazy("thisappiscalleddrown:activity_list")

    def post(self, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            form = self.form_class(self.request.POST)
            if form.is_valid():
                form.instance.user = self.request.user
                activity = Activity.objects.get(pk=self.request.POST["activity"])
                form.instance.activity_pk = activity
                activity.participants.add(self.request.user)
                form.save()
                return redirect(reverse_lazy("thisappiscalleddrown:activity_list"))
            else:
                return redirect(reverse_lazy("thisappiscalleddrown:activity_list"))
        return redirect(reverse_lazy("thisappiscalleddrown:activity_list"))

    def get_queryset(self):
        queryset = (
            Activity.objects.order_by("start_date").filter(
                Q(end_date__gte=timezone.now()) | Q(end_date__isnull=True, start_date__gte=timezone.now())
            )
            if self.request.user.is_superuser
            else Activity.objects.order_by("start_date")
            .filter(Q(group__members=self.request.user))
            .filter(Q(end_date__gte=timezone.now()) | Q(end_date__isnull=True, start_date__gte=timezone.now()))
            .filter(inscriptions__presence=True)
            .annotate(Sum("inscriptions__guests_number"), Count("inscriptions"))
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        context[
            "description"
        ] = "thisappiscalleddrown vous permet de planifier vos activit??s de groupe avec facilit?? sur le Web 2.0"
        context["form"] = InscriptionCreationForm
        return context


def save_inscription_form(request, form, template_name):
    data = dict()
    if request.method == "POST":
        # en gros je dois envoyer et sauver une instance avant de valider, si la valeur est trop haute, ne pas continuer
        # sinon tu continues, et l?? tu sauves.
        # bruh.
        # https://stackoverflow.com/questions/23361057/django-comparing-old-and-new-field-value-before-saving
        if form.is_valid():
            form.save()
            data["form_is_valid"] = True
            upcoming_activities = (
                Activity.objects.order_by("start_date")
                .filter(Q(group__members=request.user))
                .filter(Q(end_date__gte=timezone.now()) | Q(end_date__isnull=True, start_date__gte=timezone.now()))
                .filter(inscriptions__presence=True)
                .annotate(Sum("inscriptions__guests_number"), Count("inscriptions"))
            )
            data["html_upcoming_activities_list"] = render_to_string(
                "thisappiscalleddrown/partial_activity_list.html",
                {"upcoming_activities": upcoming_activities, "user": request.user},
            )
        else:
            data["form_is_valid"] = False
    context = {"form": form}
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def inscription_create(request):
    if request.method == "POST":
        form = InscriptionCreationForm(request.POST)
    else:
        form = InscriptionCreationForm()
    return save_inscription_form(request, form, "thisappiscalleddrown/partial_inscription_create.html")


def inscription_update(request, slug):
    inscription = get_object_or_404(Inscription, slug=slug)
    if request.method == "POST":
        form = InscriptionCreationForm(request.POST, instance=inscription)
    else:
        form = InscriptionCreationForm(instance=inscription)
    return save_inscription_form(request, form, "thisappiscalleddrown/partial_inscription_update.html")


def activity_clone(request, slug):
    activity = get_object_or_404(Activity, slug=slug)
    start_date = activity.start_date

    activity.start_date = start_date + datetime.timedelta(7)
    if request.method == "POST":
        form = ActivityCloneForm(request.POST, instance=activity)
    else:
        form = ActivityCloneForm(instance=activity)
    return clone_activity_form(request, form, "thisappiscalleddrown/partial_activity_clone.html")


def clone_activity_form(request, form, template_name):
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            form.save()
            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    context = {"form": form}
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


class InscriptionsTemplateView(TemplateView):
    template_name = "thisappiscalleddrown/inscription_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Inscriptions"
        context[
            "desc"
        ] = "Disclaimer: Ceci est une demo d'impl??mentation diff??rente, plus propre et plus DRY d'affichage \
            de listes d'??l??ments, et peut en soit s'utiliser pour d'autre chose que des listes. \
            le design n'est pas ?? prendre en compte et n'est pas d??finitif, il vient du copy paste."
        return context


class NotificationsView(LoginRequiredMixin, TemplateView):
    """
    Vue des notifications.

    **Contexte**

    ``title``
        Titre de la page.
    ``description``
        Description de la page.
    ``notifications``
        Notifications. Liste de :model:`thisappiscalleddrown.Notification`
    ``invitations``
        Invitations aux groupes. Liste de :model:`thisappiscalleddrown.Invitation`

    **Template**

    :template:'thisappiscalleddrown/notifications/notifications.html'
    """

    template_name = "thisappiscalleddrown/notifications/notifications.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        context["notifications"] = Notification.objects.filter(user=self.request.user).order_by("-date_sent")
        context["invitations"] = Invitation.objects.filter(user=self.request.user).order_by("-date")
        context[
            "description"
        ] = "thisappiscalleddrown vous permet de planifier vos activit??s de groupe avec facilit?? sur le Web 2.0"
        return context

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        if data["action"] == "deleteNotification":
            notification_id = data["notification"]
            notification = Notification.objects.get(id=notification_id)
            notification.delete()
            response_data = unread_notifications_number_to_dictionary(user=self.request.user)
            return JsonResponse(response_data)

        if data["action"] == "deleteAllNotifications":
            Notification.objects.filter(user=self.request.user).delete()
            return HttpResponse(status=200)


class HomeView(TemplateView):
    """
    Vue de la landing page.

    **Contexte**

    ``title``
        Titre de la page.
    ``description``
        Description de la page.

    **Template**

    :template:'thisappiscalleddrown/homepage.html'
    """

    template_name = "thisappiscalleddrown/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        context[
            "description"
        ] = "thisappiscalleddrown vous permet de planifier vos activit??s de groupe avec facilit?? sur le Web 2.0"
        return context


class ActivityDetailView(LoginRequiredMixin, DetailView):
    """
    Vue du d??tail d'une activit??.

    **Contexte**

    ``title``
        Titre de la page.
    ``description``
        Description de la page.

    **Template**

    :template:'thisappiscalleddrown/activities/activity_detail.html'
    """

    model = Activity
    template_name = "thisappiscalleddrown/activities/activity_detail.html"
    form_class = ActivityCloneForm

    def post(self, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            form = self.form_class(self.request.POST)
            activity = get_object_or_404(Activity, slug=self.kwargs["slug"])
            if form.is_valid():
                form.instance.group = activity.group
                form.instance.max_participants = activity.max_participants
                form.instance.start_location = activity.start_location
                form.instance.end_location = activity.end_location
                form.instance.description = activity.description
                form.instance.remarks = activity.remarks
                form.instance.name = activity.name
                form.instance.creator = self.request.user
                if activity.end_date:
                    difference_date = activity.end_date.day - activity.start_date.day
                    difference_time = activity.end_date.hour - activity.start_date.hour
                    form.instance.end_date = form.instance.start_date + datetime.timedelta(
                        days=difference_date, hours=difference_time
                    )
                form.instance.save()
                form.instance.participants.add(self.request.user)
                form.instance.inscriptions.create(guests_number=0, user=self.request.user)
                form.save()
                return redirect(form.instance.get_absolute_url())
            else:
                return redirect(activity.get_absolute_url())
        return redirect(reverse_lazy("thisappiscalleddrown:activity_list"))

    def get_participants_count(self):
        participants = Inscription.objects.filter(activity=self.get_object(), presence=True)
        return participants

    def get_guests_number(self):
        guests = 0
        participants = Inscription.objects.filter(activity=self.get_object(), presence=True)
        for par in participants:
            guests += par.guests_number
        return guests

    def get_total_participants_count(self):
        return self.get_participants_count().count() + self.get_guests_number()

    def get_percentage(self):
        field_name = "max_participants"
        obj = self.get_object()
        field_value = getattr(obj, field_name)
        if field_value:
            par = int(self.get_total_participants_count())
            percent = par / field_value * 100
            return round(percent)

    def get_inscriptions(self):
        return Inscription.objects.filter(Q(activity=self.get_object()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        context["description"] = "La page d??tail d'une activit??s sur thisappiscalleddrown"
        context["get_participants_count"] = self.get_participants_count()
        context["get_guests_number"] = self.get_guests_number()
        context["get_total_participants_count"] = self.get_total_participants_count()
        context["get_percentage"] = self.get_percentage()
        context["inscriptions"] = self.get_inscriptions()
        return context


class ActivityCreateView(LoginRequiredMixin, CreateView):
    """
    Vue de cr??ation d'une activit??.

    **Contexte**

    ``title``
        Titre de la page.
    ``description``
        Description de la page.

    **Template**

    :template:'thisappiscalleddrown/activities/add_activity.html'
    """

    model = Activity
    template_name = "thisappiscalleddrown/activities/add_activity.html"
    form_class = ActivityCreationForm

    def get_form_kwargs(self):
        """Passes the request object to the form class.
        This is necessary to only display members that belong to a given user"""

        kwargs = super(ActivityCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.save()
        form.instance.participants.add(self.request.user)
        form.instance.inscriptions.create(guests_number=0, user=self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        context["description"] = "Cr??er une activit?? sur thisappiscalleddrown"
        return context


class InscriptionCreateView(LoginRequiredMixin, CreateView):
    model = Inscription
    template_name = "thisappiscalleddrown/activities/create_inscription.html"
    form_class = InscriptionCreationForm

    def form_valid(self, form):
        activity = Activity.objects.get(slug=self.kwargs["slug"])
        form.instance.activity = activity
        activity.participants.add(self.request.user)
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("thisappiscalleddrown:activity_detail", kwargs={"slug": self.kwargs["slug"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        context["description"] = "Cr??er une activit?? sur thisappiscalleddrown"
        return context


class GroupActivityCreateView(LoginRequiredMixin, CreateView):
    """
    Vue de cr??ation d'une activit?? de groupe.

    **Contexte**

    ``title``
        Titre de la page.
    ``description``
        Description de la page.

    **Template**

    :template:'thisappiscalleddrown/activities/add_activity.html'
    """

    model = Activity
    template_name = "thisappiscalleddrown/activities/add_activity.html"
    form_class = ActivityCreationForm

    def get_form_kwargs(self):
        """Passes the request object to the form class.
        This is necessary to only display members that belong to a given user"""

        kwargs = super(GroupActivityCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.save()
        form.instance.participants.add(self.request.user)
        form.instance.inscriptions.create(guests_number=0, user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("thisappiscalleddrown:group_detail", kwargs={"slug": self.kwargs["slug"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        context["description"] = "Cr??er une activit?? sur thisappiscalleddrown"
        return context


class ActivityCloneView(LoginRequiredMixin, CreateView):
    """
    Vue de clonage d'une activit??.

    **Contexte**

    ``title``
        Titre de la page.
    ``description``
        Description de la page.
    ``form``
        Formulaire de cr??ation d'activit??.

    **Template**

    :template:'thisappiscalleddrown/activities/add_activity.html'
    """

    model = Activity
    template_name = "thisappiscalleddrown/activities/add_activity.html"
    form_class = ActivityCloneForm

    def get_form_kwargs(self):
        """Passes the request object to the form class.
        This is necessary to only display members that belong to a given user"""

        kwargs = super(ActivityCloneView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.save()
        form.instance.participants.add(self.request.user)
        form.instance.inscriptions.create(guests_number=0, user=self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        context["description"] = "Cr??er une activit?? sur thisappiscalleddrown"
        return context


class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vue de mise ?? jour d'une activit??.

    **Contexte**

    ``title``
        Titre de la page.
    ``description``
        Description de la page.

    **Template**

    :template:'thisappiscalleddrown/activities/update_activity.html'
    """

    model = Activity
    template_name = "thisappiscalleddrown/activities/update_activity.html"
    form_class = ActivityChangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        context["description"] = "Modifier une activit?? sur thisappiscalleddrown"
        return context


class ActivityDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vue de confirmation de suppression d'une activit??.

    **Contexte**

    ``title``
        Titre de la page.
    ``description``
        Description de la page.

    **Template**

    :template:'thisappiscalleddrown/activities/activity_confirm_delete.html'
    """

    model = Activity
    template_name = "thisappiscalleddrown/activities/activity_confirm_delete.html"
    success_url = reverse_lazy("thisappiscalleddrown:activity_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        context["description"] = "Supprime une activit?? sur thisappiscalleddrown"
        return context


class GroupListView(LoginRequiredMixin, ListView):
    """
    Vue de liste des groupes.

    **Contexte**

    ``title``
        Titre de la page.
    ``description``
        Description de la page.

    **Template**

    :template:'thisappiscalleddrown/groups/group_list.html'
    """

    template_name = "thisappiscalleddrown/groups/group_list.html"
    model = Group

    def get_queryset(self):
        if not self.request.user.is_superuser:
            self.groups = self.model.objects.filter(members=self.request.user)
        else:
            self.groups = self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        context["description"] = "La liste des groupes sur thisappiscalleddrown"
        context["groups"] = self.groups
        return context


class GroupDetailView(LoginRequiredMixin, DetailView):
    """
    Vue de liste des groupes.

    **Contexte**

    ``title``
        Titre de la page.
    ``description``
        Description de la page.
    ``members``
        Membres du groupe. Liste de :model:``accounts.CustomUser``
    ``admins``
        Administrateurs du groupe. Liste de :model:``accounts.CustomUser``
    ``all_members``
        Tous les membres, incluant les administrateurs. Liste de :model:``accounts.CustomUser``
    ``members_count``
        Nombre de membres.
    ``undisplayed_members_count``
        Nombre de membres non affich??s.
    ``upcoming_activities``
        Activit??s de groupes futures. Liste de :model:`thisappiscalleddrown.Activity`
    ``invitation_form``
        Formulaire d'invitation.

    **Template**

    :template:'thisappiscalleddrown/groups/group_detail.html'
    """

    model = Group
    template_name = "thisappiscalleddrown/groups/group_detail.html"
    context_object_name = "group"

    def get_activities_by_group(self):
        return (
            Activity.objects.filter(group=self.get_object())
            .filter(start_date__gte=timezone.now())
            .order_by("start_date")
        )

    def get_past_activities_by_group(self):
        return (
            Activity.objects.filter(group=self.get_object())
            .filter(start_date__lt=timezone.now())
            .order_by("start_date")
        )

    def get_global_invitation_or_create(self):
        if Invitation.objects.filter(slug=self.get_object().slug).exists():
            return Invitation.objects.get(slug=self.get_object().slug)
        else:
            invitation = Invitation.objects.create(sender=None, group=self.get_object(), slug=self.get_object().slug)
            invitation.save()
            return invitation

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        if data["action"] == "join":
            self.get_object().members.add(self.request.user)
            return HttpResponse(status=200)
        elif data["action"] == "leave":
            self.get_object().members.remove(self.request.user)
            return HttpResponse(status=200)
        elif data["action"] == "getInvitationLink":
            invitation = self.get_global_invitation_or_create()
            return JsonResponse({"invitationLink": invitation.get_absolute_url()})
        elif data["action"] == "invite":
            form = InvitationCreationForm(data["form"])

            if form.is_valid():
                if CustomUser.objects.filter(email=form.cleaned_data.get("email")).count() > 0:
                    user = CustomUser.objects.get(email=form.cleaned_data.get("email"))
                    group = self.get_object()

                    if user in group.members.all() or user in group.admins.all():
                        message = {
                            "text": "Cet utilisateur appartient d??j?? ?? ce groupe.",
                            "severity": "ERROR",
                        }
                    else:
                        if (
                            Invitation.objects.filter(sender=self.request.user).count()
                            <= MAX_INVITATION_NUMBER_BY_USER
                        ):
                            if Invitation.objects.filter(user=user, group=group).count() == 0:
                                invitation = Invitation(user=user, sender=self.request.user, group=group)
                                invitation.save()
                                message = {
                                    "text": "Invitation envoy??e.",
                                    "severity": "SUCCESS",
                                }
                            else:
                                message = {
                                    "text": "Cet utilisateur a d??j?? ??t?? invit?? ?? ce groupe.",
                                    "severity": "ERROR",
                                }
                        else:
                            message = {
                                "text": "Vous avez atteint la limite du nombre d'invitation par utilisateur. Veuillez r??essayer plus tard.",
                                "severity": "ERROR",
                            }

                else:
                    message = {
                        "text": "La personne n'a pas de compte thisappiscalleddrown. Vous pouvez lui envoyer un lien d'invitation.",
                        "severity": "ERROR",
                    }
                response_data = {
                    "message": message,
                }
                return JsonResponse(response_data)
            else:
                message = {
                    "text": "Les champs du formulaires ne sont pas valides.",
                    "severity": "ERROR",
                }
                response_data = {"message": message}
                return JsonResponse(response_data)

    def get_context_data(self, **kwargs):
        admins = self.get_object().admins.distinct()
        admin_ids = admins.values_list("id", flat=True)
        members = self.get_object().members.distinct().exclude(id__in=admin_ids)
        all_members_count = Count(members) + Count(admins)

        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        context["description"] = self.get_object().description
        context["members"] = members
        context["admins"] = admins
        context["all_members"] = members | admins
        context["members_count"] = all_members_count
        context["undisplayed_members_count"] = all_members_count - 10
        context["upcoming_activities"] = self.get_activities_by_group()
        context["past_activities"] = self.get_past_activities_by_group()
        context["invitation_form"] = InvitationCreationForm
        return context


class InvitationView(DetailView):
    """
    Vue d'invitation ?? un groupe'.

    **Contexte**

    ``title``
        Titre de la page.
    ``description``
        Description de la page.

    **Template**

    :template:'thisappiscalleddrown/groups/invitation.html'
    """

    template_name = "thisappiscalleddrown/groups/invitation.html"
    model = Invitation
    context_object_name = "invitation"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        context["description"] = f"Invitation au groupe {self.get_object().group}"
        return context

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            self.request.session["invitation"] = self.get_object().slug
            return redirect(f"{reverse('account:login')}?next={self.get_object().get_absolute_url()}")

        if self.request.user in self.get_object().group.members.filter(member__id=self.request.user.id) != 0:
            messages.error(request=self.request, message="Vous faites d??j?? partie de ce groupe.")
            return redirect(reverse("thisappiscalleddrown:activity_list"))

        if self.get_object().user and self.request.user != self.get_object().user:
            messages.error(
                request=self.request,
                message="Cette invitation ne vous est pas destin??e.",
            )
            return redirect(reverse("thisappiscalleddrown:activity_list"))

        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        group = self.get_object().group
        if not self.get_object().user or self.request.user == self.get_object().user:
            if self.request.POST.get("accept"):
                self.get_object().group.members.add(self.request.user)
                if self.get_object().user:
                    self.model.objects.get(id=self.get_object().id).delete()
                messages.success(
                    request=self.request,
                    message=f"Vous faites d??sormais partie du groupe {group.name}.",
                )
                return redirect(reverse("thisappiscalleddrown:group_detail", kwargs={"slug": group.slug}))
            elif self.request.POST.get("decline"):
                messages.success(
                    request=self.request,
                    message=f"Vous avez d??clin?? l'invitation au groupe {group.name}.",
                )
                if self.get_object().user:
                    self.model.objects.get(id=self.request.user.id).delete()
                return redirect(reverse("thisappiscalleddrown:activity_list"))
        else:
            messages.error(
                request=self.request,
                message="Cette invitation ne vous est pas destin??e.",
            )
            return redirect(reverse("thisappiscalleddrown:activity_list"))


class InscriptionView(DetailView):
    """
    Vue d'invitation ?? un groupe'.

    **Contexte**

    ``title``
        Titre de la page.
    ``description``
        Description de la page.

    **Template**

    :template:'thisappiscalleddrown/activities/inscription.html'
    """

    template_name = "thisappiscalleddrown/activities/inscription.html"
    model = Inscription
    context_object_name = "inscription"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        return context


class GroupCreateView(LoginRequiredMixin, CreateView):
    """
    Vue de cr??ation de groupe.

    **Contexte**

    ``title``
        Titre de la page.
    ``description``
        Description de la page.

    **Template**

    :template:'thisappiscalleddrown/groups/add_group.html'
    """

    template_name = "thisappiscalleddrown/groups/add_group.html"
    form_class = CustomGroupCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        context["description"] = "Cr??er un groupe sur thisappiscalleddrown"
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.admins.add(self.request.user)
        self.object.members.add(self.request.user)
        return redirect(self.get_success_url())


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vue de mise ?? jour de groupe.

    **Contexte**

    ``title``
        Titre de la page.
    ``description``
        Description de la page.

    **Template**

    :template:'thisappiscalleddrown/groups/update_group.html'
    """

    model = Group
    template_name = "thisappiscalleddrown/groups/update_group.html"
    form_class = CustomGroupChangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        context["description"] = "Modifier un groupe sur thisappiscalleddrown"
        return context


class GroupDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vue de suppression de groupe.

    **Contexte**

    ``title``
        Titre de la page.
    ``description``
        Description de la page.

    **Template**

    :template:'thisappiscalleddrown/groups/group_confirm_delete.html'
    """

    model = Group
    template_name = "thisappiscalleddrown/groups/group_confirm_delete.html"
    success_url = reverse_lazy("thisappiscalleddrown:group_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        context["description"] = "Supprimer un groupe sur thisappiscalleddrown"
        return context


class ContributorsView(TemplateView):
    """
    Vue de suppression de groupe.

    **Contexte**

    ``title``
        Titre de la page.
    ``description``
        Description de la page.
    ``contributors``
        Contributeurs ?? thisappiscalleddrown.

    **Template**

    :template:'thisappiscalleddrown/contributors.html'
    """

    template_name = "thisappiscalleddrown/contributors.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contributors"] = CONTRIBUTORS
        context["title"] = "Compte thisappiscalleddrown"
        context["description"] = "Contributeurs du site thisappiscalleddrown"
        return context


class ConditionsView(TemplateView):
    """
    Vue de suppression de groupe.

    **Contexte**

    ``title``
        Titre de la page.
    ``description``
        Description de la page.
    ``contributors``
        Contributeurs ?? thisappiscalleddrown.

    **Template**

    :template:'thisappiscalleddrown/contributors.html'
    """

    template_name = "thisappiscalleddrown/conditions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        context["description"] = "Conditions g??n??rales d'utilisation de thisappiscalleddrown."
        return context


class ConfidentialityView(TemplateView):
    """
    Vue de confidentialit??.

    **Contexte**

    ``title``
        Titre de la page.
    ``description``
        Description de la page.
    ``contributors``
        Contributeurs ?? thisappiscalleddrown.

    **Template**

    :template:'thisappiscalleddrown/confidentiality.html'
    """

    template_name = "thisappiscalleddrown/confidentiality.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        context["description"] = "Confidentialit?? de thisappiscalleddrown"
        return context


class LicenseView(TemplateView):
    """
    Vue des licences.

    **Contexte**

    ``title``
        Titre de la page.
    ``description``
        Description de la page.

    **Template**

    :template:'thisappiscalleddrown/licenses.html'
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "thisappiscalleddrown"
        context["description"] = "Licenses"
        return context

    template_name = "thisappiscalleddrown/licenses.html"
