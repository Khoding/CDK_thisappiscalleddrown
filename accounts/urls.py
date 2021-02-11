from django.conf.urls import url
from django.contrib.auth.views import PasswordChangeView
from django.urls import path, include

from accounts.views import CustomSignUpView, EditUserProfileView, UserProfileView, UserLoginView, UserLogoutView

app_name = 'account'

urlpatterns = [
    path('signup/', CustomSignUpView.as_view(), name='signup'),
    path('edit_profile/<slug:slug>/', EditUserProfileView.as_view(), name='edit_profile'),
    path('profile/<slug:slug>/', UserProfileView.as_view(), name='profile'),
    path('password/', PasswordChangeView.as_view()),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

]
