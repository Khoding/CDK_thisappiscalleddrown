"""
Fichier des formulaires de Koolapic. Contient tout ce qui est en rapport aux formulaires, tels que :
* les inputs
* les widgets
* les formulaires
"""

from django import forms
from django.core import validators
from django.core.validators import FileExtensionValidator
from django.forms import TextInput, ImageField, CharField

from utils.image_utils import crop_redim_image
from koolapic.models import Activity, Group, Invitation

from bootstrap_datepicker_plus import DateTimePickerInput
from easy_maps.widgets import AddressWithMapWidget

VALID_IMAGE_EXTENSIONS = [
    'bmp', 'gif', 'png', 'apng', 'jpg', 'jpeg'
]


class ImageCropField(ImageField):
    """
    Champ de formulaire permettant de rogner les images avant leur import.
    """

    default_validators = [validators.validate_image_file_extension, FileExtensionValidator(allowed_extensions=VALID_IMAGE_EXTENSIONS)]


class ActivityCreationForm(forms.ModelForm):
    """
    Formulaire de création des activités.
    """

    end_location = CharField()
    max_participants = CharField()
    end_inscription_date = CharField()
    end_date = CharField()

    end_location.is_spoiler = True
    max_participants.is_spoiler = True
    end_inscription_date.is_spoiler = True
    end_date.is_spoiler = True

    class Meta:
        model = Activity
        fields = [
            'name',
            'has_no_group',
            'group',

            'description',
            'remarks',

            'start_location',
            'start_date',
            'inscription_policy',

            'end_inscription_date',
            'max_participants',
            'accompagnants',
            'end_location',
            'end_date',
        ]

        widgets = {
            'group': forms.Select(attrs={'class': 'col-8'}),
            'end_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'start_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'last_update': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'end_inscription_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'address': AddressWithMapWidget({'class': 'vTextField'}),
        }


class ActivityChangeForm(forms.ModelForm):
    """
    Formulaire de modification des activités.
    """

    class Meta:
        model = Activity
        fields = [
            'name',
            'inscription_policy',
            'end_inscription_date',
            'description',
            'remarks',
            'accompagnants',
            'max_participants',

            'start_location',
            'start_date',

            'end_location',
            'end_date',
        ]

        widgets = {
            'end_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'start_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'last_update': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'end_inscription_date': DateTimePickerInput(format='%d/%m/%Y %H:%M'),
            'address': AddressWithMapWidget({'class': 'vTextField'})
        }


class CustomGroupCreationForm(forms.ModelForm):
    """
    Formulaire de création de groupe Koolapic.
    """

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

            crop_redim_image((x, y, w, h), (1072, 272), custom_group.image.path)
        return custom_group


class CustomGroupChangeForm(forms.ModelForm):
    """
    Formulaire de changement de groupe de Koolapic.
    """

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
        """
        Fonction appelée à la sauvegarde du formulaire.
        Récupère les données du rognage et rogne l'image.
        """

        custom_group = super(CustomGroupChangeForm, self).save()
        if self.cleaned_data.get('width'):
            x = self.cleaned_data.get('x')
            y = self.cleaned_data.get('y')
            w = self.cleaned_data.get('width')
            h = self.cleaned_data.get('height')

            crop_redim_image((x, y, w, h), (1072, 272), custom_group.image.path)
        return custom_group


class InvitationCreationForm(forms.ModelForm):
    """
    Formulaire de création d'invitations.
    """

    email = forms.EmailField(required=True)
    link = forms.CharField(required=False)

    class Meta:
        model = Invitation
        fields = ('email', 'link')
