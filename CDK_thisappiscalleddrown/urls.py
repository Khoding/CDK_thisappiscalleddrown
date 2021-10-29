"""CDK_thisappiscalleddrown URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from thisappiscalleddrown.views import ContributorsView, IndexView, LicenseView, NotificationsView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import accounts.urls
import thisappiscalleddrown.urls
import thisappiscalleddrownAPI.urls
from CDK_thisappiscalleddrown import dev_urls

app_name = "admin"

admin.site.site_header = "thisappiscalleddrown Admin"
admin.site.site_title = "thisappiscalleddrown"
admin.site.index_title = "Administration de thisappiscalleddrown"

urlpatterns = [
    path("", include(thisappiscalleddrown.urls)),
    path("conditions/", IndexView.as_view(), name="conditions"),
    path("confidentiality/", IndexView.as_view(), name="confidentiality"),
    path("licenses/", LicenseView.as_view(), name="licenses"),
    path("notifications/", NotificationsView.as_view(), name="notifications"),
    path("contributors/", ContributorsView.as_view(), name="contributors"),
    path("admin/", admin.site.urls),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("api/", include(thisappiscalleddrownAPI.urls, namespace="api")),
    path("accounts/", include(accounts.urls, namespace="account")),
    path("dev/", include(dev_urls, namespace="dev")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
