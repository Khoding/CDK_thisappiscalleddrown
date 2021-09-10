"""
URLs de l'application Koolapic.
"""

from django.urls import path

from koolapic.views import (ActivityCloneView, ActivityCreateView,
                            ActivityDeleteView, ActivityDetailView,
                            ActivityUpdateView, GroupActivityCreateView,
                            GroupCreateView, GroupDeleteView, GroupDetailView,
                            GroupListView, GroupUpdateView, HomeView,
                            IndexView, InscriptionCreateView,
                            InscriptionsTemplateView, InscriptionView,
                            InvitationView, inscription_create,
                            inscription_update)

from .feeds import GroupActivityFeed

app_name = 'koolapic'

urlpatterns = [
    path('', HomeView.as_view(), name='homepage'),
    path('app/', IndexView.as_view(), name='activity_list'),

    path('invitation/<slug:slug>/', InvitationView.as_view(), name='invitation'),

    path('inscription/', InscriptionsTemplateView.as_view(),
         name='inscription_list'),
    path('inscription/<slug:slug>/', InscriptionView.as_view(), name='inscription'),

    path('ajax/inscription/create/',
         inscription_create, name='create_inscription_ajax'),
    path('ajax/inscription/<slug:slug>/update/',
         inscription_update, name='update_inscription_ajax'),

    path('activity/add/', ActivityCreateView.as_view(), name="add_activity"),
    path('activity/<slug:slug>/',
         ActivityDetailView.as_view(), name="activity_detail"),
    path('activity/<slug:slug>/inscription/',
         InscriptionCreateView.as_view(), name='activity_inscription'),
    path('activity/<slug:slug>/clone/',
         ActivityCloneView.as_view(), name="clone_activity"),
    path('activity/<slug:slug>/update/',
         ActivityUpdateView.as_view(), name="update_activity"),
    path('activity/<slug:slug>/confirm_delete/',
         ActivityDeleteView.as_view(), name="activity_confirm_delete"),

    path('groups/', GroupListView.as_view(), name="group_list"),
    path('groups/add/', GroupCreateView.as_view(), name="add_group"),
    path('groups/<slug:slug>/', GroupDetailView.as_view(), name="group_detail"),
    path('groups/<slug:slug>/rss/', GroupActivityFeed(),
         name="group_activity_feed"),
    path('groups/<slug:slug>/update/',
         GroupUpdateView.as_view(), name="update_group"),
    path('groups/<slug:slug>/confirm_delete/',
         GroupDeleteView.as_view(), name="group_confirm_delete"),
    path('groups/<slug:slug>/activity/add/',
         GroupActivityCreateView.as_view(), name="group_activity_add"),
]
