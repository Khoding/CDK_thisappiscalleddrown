from django.urls import path
from .views import SignUpView, LoginView, UserEditView, UserProfileView, PasswordsChangeView


app_name = 'users'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('edit_profile/<slug:slug>/', UserEditView.as_view(), name='edit_profile'),
    path('profile/<slug:slug>/', UserProfileView.as_view(), name='profile'),
    path('password/', PasswordsChangeView.as_view()),

]
