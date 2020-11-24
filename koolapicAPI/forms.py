from django import forms
from django.forms import TextInput

from .models import Activity, Admission, Group, Inscription

from bootstrap_datepicker_plus import DateTimePickerInput
# TODO pas encore fini
from easy_maps.widgets import AddressWithMapWidget
# TODO pas encore fini


class CustomActivityCreationForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = "__all__"
        exclude = ('slug',)

        widgets = {
            'end_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'start_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'last_update': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'end_inscription_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            # TODO pas encore fini
            'address': AddressWithMapWidget({'class': 'vTextField'})
            # TODO pas encore fini
        }


class CustomActivityChangeForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        exclude = ('slug',)

        widgets = {
            'end_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'start_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'last_update': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'end_inscription_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            # TODO pas encore fini
            'address': AddressWithMapWidget({'class': 'vTextField'})
            # TODO pas encore fini
        }


class CustomGroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "__all__"
        exclude = ('slug', 'admission')

        widgets = {
            'banner_color': TextInput(attrs={'type': 'color'}),
            'date_don': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
        }


class CustomGroupChangeForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        exclude = ('slug', 'admission')

        widgets = {
            'banner_color': TextInput(attrs={'type': 'color'}),
            'date_don': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
        }
