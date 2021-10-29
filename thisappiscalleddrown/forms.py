"""
Fichier des formulaires de thisappiscalleddrown. Contient tout ce qui est en rapport aux formulaires, tels que :
* les inputs
* les widgets
* les formulaires
"""

from django import forms
from django.core import validators
from django.core.validators import FileExtensionValidator
from django.forms import ImageField, TextInput
from easy_maps.widgets import AddressWithMapWidget
from utils.image_utils import crop_redim_image

from thisappiscalleddrown.models import Activity, Group, Inscription, Invitation

VALID_IMAGE_EXTENSIONS = ["bmp", "gif", "png", "apng", "jpg", "jpeg"]


class ImageCropField(ImageField):
    """
    Champ de formulaire permettant de rogner les images avant leur import.
    """

    default_validators = [
        validators.validate_image_file_extension,
        FileExtensionValidator(allowed_extensions=VALID_IMAGE_EXTENSIONS),
    ]


class ActivityCreationForm(forms.ModelForm):
    """
    Formulaire de création des activités.
    """

    start_date = forms.SplitDateTimeField(
        input_date_formats=["%Y-%m-%d"],
        input_time_formats=["%H:%M:%S", "%H:%M"],
        widget=forms.SplitDateTimeWidget(
            date_attrs={"type": "date"},
            date_format="%Y-%m-%d",
            time_attrs={"type": "time"},
            time_format="%H:%M:%S",
        ),
        label="Date de début",
    )
    end_date = forms.SplitDateTimeField(
        required=False,
        input_date_formats=["%Y-%m-%d"],
        input_time_formats=["%H:%M:%S", "%H:%M"],
        widget=forms.SplitDateTimeWidget(
            date_attrs={"type": "date"},
            date_format="%Y-%m-%d",
            time_attrs={"type": "time"},
            time_format="%H:%M:%S",
        ),
        label="Date de fin",
    )

    group = forms.Select()

    def __init__(self, **kwargs):
        self.request = kwargs.pop("request")
        super(ActivityCreationForm, self).__init__(**kwargs)
        self.fields["group"].queryset = Group.objects.filter(members=self.request.user)

    class Meta:
        model = Activity
        fields = [
            "name",
            "group",
            "description",
            "remarks",
            "start_location",
            "start_date",
            "max_participants",
            "end_location",
            "end_date",
        ]

        widgets = {
            "address": AddressWithMapWidget({"class": "vTextField"}),
        }


class ActivityOldCloneForm(forms.ModelForm):
    """
    Formulaire de clonage des activités.
    """

    start_date = forms.SplitDateTimeField(
        input_date_formats=["%Y-%m-%d"],
        input_time_formats=["%H:%M:%S", "%H:%M"],
        widget=forms.SplitDateTimeWidget(
            date_attrs={"type": "date"},
            date_format="%Y-%m-%d",
            time_attrs={"type": "time"},
            time_format="%H:%M:%S",
        ),
        label="Date de début",
    )
    end_date = forms.SplitDateTimeField(
        required=False,
        input_date_formats=["%Y-%m-%d"],
        input_time_formats=["%H:%M:%S", "%H:%M"],
        widget=forms.SplitDateTimeWidget(
            date_attrs={"type": "date"},
            date_format="%Y-%m-%d",
            time_attrs={"type": "time"},
            time_format="%H:%M:%S",
        ),
        label="Date de fin",
    )

    exclude = [
        "participants",
    ]

    group = forms.Select()

    # initial

    def __init__(self, **kwargs):
        self.request = kwargs.pop("request")
        super(ActivityOldCloneForm, self).__init__(**kwargs)
        self.fields["group"].queryset = Group.objects.filter(members=self.request.user)

    class Meta:
        model = Activity
        fields = [
            "name",
            "group",
            "description",
            "remarks",
            "start_location",
            "start_date",
            "max_participants",
            "end_location",
            "end_date",
        ]

        widgets = {
            "address": AddressWithMapWidget({"class": "vTextField"}),
        }


class ActivityCloneForm(forms.ModelForm):
    """
    Formulaire de clonage des activités.
    """

    start_date = forms.SplitDateTimeField(
        input_date_formats=["%Y-%m-%d"],
        input_time_formats=["%H:%M:%S", "%H:%M"],
        widget=forms.SplitDateTimeWidget(
            date_attrs={"type": "date"},
            date_format="%Y-%m-%d",
            time_attrs={"type": "time"},
            time_format="%H:%M:%S",
        ),
        label="Date de début",
    )

    class Meta:
        model = Activity
        fields = [
            "start_date",
        ]


class ActivityChangeForm(forms.ModelForm):
    """
    Formulaire de modification des activités.
    """

    start_date = forms.SplitDateTimeField(
        input_date_formats=["%Y-%m-%d"],
        input_time_formats=["%H:%M:%S", "%H:%M"],
        widget=forms.SplitDateTimeWidget(
            date_attrs={"type": "date"},
            date_format="%Y-%m-%d",
            time_attrs={"type": "time"},
            time_format="%H:%M:%S",
        ),
        label="Date de début",
    )
    end_date = forms.SplitDateTimeField(
        required=False,
        input_date_formats=["%Y-%m-%d"],
        input_time_formats=["%H:%M:%S", "%H:%M"],
        widget=forms.SplitDateTimeWidget(
            date_attrs={"type": "date"},
            date_format="%Y-%m-%d",
            time_attrs={"type": "time"},
            time_format="%H:%M:%S",
        ),
        label="Date de fin",
    )

    class Meta:
        model = Activity
        fields = [
            "name",
            "description",
            "remarks",
            "start_location",
            "start_date",
            "max_participants",
            "end_location",
            "end_date",
        ]

        widgets = {
            "address": AddressWithMapWidget({"class": "vTextField"}),
        }


class CustomGroupCreationForm(forms.ModelForm):
    """
    Formulaire de création de groupe thisappiscalleddrown.
    """

    x = forms.FloatField(widget=forms.HiddenInput, required=False)
    y = forms.FloatField(widget=forms.HiddenInput, required=False)
    width = forms.FloatField(widget=forms.HiddenInput, required=False)
    height = forms.FloatField(widget=forms.HiddenInput, required=False)
    image = ImageCropField(required=False, label="Image du groupe")

    class Meta:
        model = Group
        fields = (
            "name",
            "description",
            "banner_color",
            "image",
            "x",
            "y",
            "width",
            "height",
        )

        widgets = {
            "banner_color": TextInput(attrs={"type": "color"}),
        }

    def save(self, *args, **kwargs):
        custom_group = super(CustomGroupCreationForm, self).save()
        if self.cleaned_data.get("width"):
            x = self.cleaned_data.get("x")
            y = self.cleaned_data.get("y")
            w = self.cleaned_data.get("width")
            h = self.cleaned_data.get("height")

            crop_redim_image((x, y, w, h), (1072, 272), custom_group.image.path)
        return custom_group


class CustomGroupChangeForm(forms.ModelForm):
    """
    Formulaire de changement de groupe de thisappiscalleddrown.
    """

    x = forms.FloatField(widget=forms.HiddenInput, required=False)
    y = forms.FloatField(widget=forms.HiddenInput, required=False)
    width = forms.FloatField(widget=forms.HiddenInput, required=False)
    height = forms.FloatField(widget=forms.HiddenInput, required=False)
    image = ImageCropField(required=False, label="Image du groupe")

    class Meta:
        model = Group
        fields = (
            "name",
            "description",
            "banner_color",
            "admins",
            "members",
            "image",
            "x",
            "y",
            "width",
            "height",
        )

        widgets = {
            "banner_color": TextInput(attrs={"type": "color"}),
        }

    def save(self, *args, **kwargs):
        """
        Fonction appelée à la sauvegarde du formulaire.
        Récupère les données du rognage et rogne l'image.
        """

        custom_group = super(CustomGroupChangeForm, self).save()
        if self.cleaned_data.get("width"):
            x = self.cleaned_data.get("x")
            y = self.cleaned_data.get("y")
            w = self.cleaned_data.get("width")
            h = self.cleaned_data.get("height")

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
        fields = ("email", "link")


class InscriptionCreationForm(forms.ModelForm):
    """
    Formulaire de création d'inscriptions.
    """

    class Meta:
        model = Inscription
        fields = (
            "remarks",
            "presence",
            "guests_number",
            "activity",
        )
