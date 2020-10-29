from django import forms
from .models import Activity, Admission, Group, Inscription


class CustomActivityCreationForm(forms.ModelForm):

    class Meta:
        model = Activity
        fields = "__all__"
        exclude = ('slug',)
