"""
URLs de l'application Accounts.
"""

from django.contrib.auth.views import PasswordChangeView
from django.urls import path

from accounts.views import SignupView, EditUserProfileView, UserProfileView, UserLoginView, UserLogoutView

app_name = 'account'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('edit_profile/<slug:slug>/', EditUserProfileView.as_view(), name='edit_profile'),
    path('profile/<slug:slug>/', UserProfileView.as_view(), name='profile'),
    path('password/', PasswordChangeView.as_view()),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

]
