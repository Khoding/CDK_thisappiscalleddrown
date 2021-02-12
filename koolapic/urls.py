from django.urls import path

from koolapic.views import ActivityListView, ActivityCreateView, ActivityDetailView, ActivityUpdateView, \
    ActivityDeleteView, \
    GroupListView, GroupCreateView, GroupDetailView, GroupUpdateView, GroupDeleteView, ActivityCloneView, \
    NotificationsView, InvitationView, LicenseView, GroupActivityCreateView, ContributorsView
from koolapic.views import IndexView, HomeView

app_name = 'koolapic'

urlpatterns = [
    path('', HomeView.as_view(), name='homepage'),
    path('app/', IndexView.as_view(), name='home'),
    path('conditions/', IndexView.as_view(), name='conditions'),
    path('confidentiality/', IndexView.as_view(), name='confidentiality'),
    path('licenses/', LicenseView.as_view(), name='licenses'),
    path('notifications/', NotificationsView.as_view(), name='notifications'),
    path('contributors/', ContributorsView.as_view(), name='contributors'),
    path('invitation/<slug:slug>/', InvitationView.as_view(), name='invitation'),

    path('activities/', ActivityListView.as_view(), name="activity_list"),
    path('activities/<slug:slug>/', ActivityDetailView.as_view(), name="activity_detail"),
    path('activities/add', ActivityCreateView.as_view(), name="add_activity"),
    path('activities/<slug:slug>/clone', ActivityCloneView.as_view(), name="clone_activity"),
    path('activities/<slug:slug>/update/', ActivityUpdateView.as_view(), name="update_activity"),
    path('activities/<slug:slug>/confirm_delete/', ActivityDeleteView.as_view(), name="activity_confirm_delete"),


    path('groups/', GroupListView.as_view(), name="group_list"),
    path('groups/<slug:slug>/', GroupDetailView.as_view(), name="group_detail"),
    path('groups/add', GroupCreateView.as_view(), name="add_group"),
    path('groups/<slug:slug>/update/', GroupUpdateView.as_view(), name="update_group"),
    path('groups/<slug:slug>/confirm_delete/', GroupDeleteView.as_view(), name="group_confirm_delete"),
    path('groups/<slug:slug>/activities/add', GroupActivityCreateView.as_view(), name="group_activity_add"),
]
