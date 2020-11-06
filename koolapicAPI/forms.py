from django import forms
from django.forms import TextInput

from .models import Activity, Admission, Group, Inscription


class CustomActivityCreationForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = "__all__"
        exclude = ('slug',)


class CustomActivityChangeForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        exclude = ('slug',)


class CustomGroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "__all__"
        exclude = ('slug',)
        widgets = {
            'banner_color': TextInput(attrs={'type': 'color'}),
        }


class CustomGroupChangeForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        exclude = ('slug',)
        widgets = {
            'banner_color': TextInput(attrs={'type': 'color'}),
        }
