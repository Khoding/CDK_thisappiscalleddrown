from django.contrib import admin
from .models import User, Activity, Group, Inscription, Admission


# Register your models here.

admin.site.register(User)
admin.site.register(Activity)
admin.site.register(Group)
admin.site.register(Inscription)
admin.site.register(Admission)
