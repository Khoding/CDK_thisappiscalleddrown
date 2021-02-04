import form as form
from ckeditor.fields import RichTextFormField
from django import forms
from django.core import validators
from django.core.validators import FileExtensionValidator
from django.forms import TextInput, ImageField, ModelForm

from utils.image_utils import crop_image
from koolapic.models import Activity, Group, Invitation

from bootstrap_datepicker_plus import DateTimePickerInput
from easy_maps.widgets import AddressWithMapWidget


VALID_IMAGE_EXTENSIONS = [
    'bmp', 'gif', 'png', 'apng', 'jpg', 'jpeg'
]


class ImageCropField(ImageField):
    default_validators = [validators.validate_image_file_extension, FileExtensionValidator(allowed_extensions=VALID_IMAGE_EXTENSIONS)]


class ActivityCreationForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'description', 'remarks', 'max_participants', 'start_location', 'start_date', 'end_location', 'end_date']

        widgets = {
            'end_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'start_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'last_update': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'end_inscription_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            # TODO pas encore fini
        }


class CustomGroupActivityCreationForm(forms.ModelForm):
    remarks = RichTextFormField(config_name="my-custom-toolbar")

    class Meta:
        model = Activity
        fields = ('name', "end_inscription_date", "start_location", "start_date", "description", "end_location", "end_date", "remarks", "max_participants", "participants",)

        widgets = {
            'end_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'start_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'last_update': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'end_inscription_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'address': AddressWithMapWidget({'class': 'vTextField'})
        }


class ActivityChangeForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'description', 'remarks', 'max_participants', 'start_location', 'start_date', 'end_location', 'end_date']

        widgets = {
            'end_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'start_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'last_update': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'end_inscription_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'address': AddressWithMapWidget({'class': 'vTextField'})
        }


class CustomGroupCreationForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput, required=False)
    y = forms.FloatField(widget=forms.HiddenInput, required=False)
    width = forms.FloatField(widget=forms.HiddenInput, required=False)
    height = forms.FloatField(widget=forms.HiddenInput, required=False)
    image = ImageCropField(required=False, label="Image du groupe")

    class Meta:
        model = Group
        fields = ('name', 'description', 'visibility', 'invitation_policy', 'banner_color', 'image', 'x', 'y', 'width', 'height')

        widgets = {
            'banner_color': TextInput(attrs={'type': 'color'}),
        }

    def save(self, *args, **kwargs):
        custom_group = super(CustomGroupCreationForm, self).save()
        if self.cleaned_data.get('width'):
            x = self.cleaned_data.get('x')
            y = self.cleaned_data.get('y')
            w = self.cleaned_data.get('width')
            h = self.cleaned_data.get('height')

            crop_image((x, y, w, h), (1072, 272), custom_group.image.path)
        return custom_group


class CustomGroupChangeForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput, required=False)
    y = forms.FloatField(widget=forms.HiddenInput, required=False)
    width = forms.FloatField(widget=forms.HiddenInput, required=False)
    height = forms.FloatField(widget=forms.HiddenInput, required=False)
    image = ImageCropField(required=False, label="Image du groupe")

    class Meta:
        model = Group
        fields = ('name', 'description', 'visibility', 'invitation_policy', 'banner_color', 'admins', 'members', 'banned_users', 'image', 'x', 'y', 'width', 'height')

        widgets = {
            'banner_color': TextInput(attrs={'type': 'color'}),
        }

    def save(self, *args, **kwargs):
        custom_group = super(CustomGroupChangeForm, self).save()
        if self.cleaned_data.get('width'):
            x = self.cleaned_data.get('x')
            y = self.cleaned_data.get('y')
            w = self.cleaned_data.get('width')
            h = self.cleaned_data.get('height')

            crop_image((x, y, w, h), (1072, 272), custom_group.image.path)
        return custom_group


class InvitationCreationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    link = forms.CharField(required=False)

    class Meta:
        model = Invitation
        fields = ('email', 'link')
