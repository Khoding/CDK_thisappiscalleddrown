from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'slug']

    prepopulated_fields = {'slug': ('username',)}


admin.site.register(CustomUser, CustomUserAdmin)
