from django import forms
from django.forms import TextInput

from .models import Activity, Admission, Group, Inscription

from bootstrap_datepicker_plus import DateTimePickerInput


class CustomActivityCreationForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = "__all__"
        exclude = ('slug', 'user')

        widgets = {
            'end_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'start_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'last_update': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'end_inscription_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
        }


class CustomActivityChangeForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        exclude = ('slug', 'user')


class CustomGroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "__all__"
        exclude = ('slug', 'admission')
        widgets = {
            'banner_color': TextInput(attrs={'type': 'color'}),
        }


class CustomGroupChangeForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        exclude = ('slug', 'admission')
        widgets = {
            'banner_color': TextInput(attrs={'type': 'color'}),
        }
