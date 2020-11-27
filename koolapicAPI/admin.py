from django.contrib import admin
from koolapicAPI.models import Activity, Group, Inscription, Admission


class ActivityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Inscription)
admin.site.register(Admission)
