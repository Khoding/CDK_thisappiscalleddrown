from django.contrib import admin
from koolapicAPI.models import Activity, Group, Inscription, Admission


class ActivityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('description',)}


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Group)
admin.site.register(Inscription)
admin.site.register(Admission)
