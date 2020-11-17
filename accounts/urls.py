from django.urls import path
from .views import SignUpView, UserEditView, UserProfileView, PasswordsChangeView

app_name = 'users'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password/', PasswordsChangeView.as_view()),
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout')
]
