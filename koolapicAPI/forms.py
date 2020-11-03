from django import forms
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


class CustomGroupChangeForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        exclude = ('slug',)
