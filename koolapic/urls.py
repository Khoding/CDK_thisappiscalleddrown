from django.urls import path, include

from koolapic.views import IndexView, SignUpView, KoolapicLoginView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('index/', IndexView.as_view(), name='index'),
    path('home/', IndexView.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', KoolapicLoginView.as_view(), name='login'),
]
