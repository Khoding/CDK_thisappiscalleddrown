from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.core.validators import FileExtensionValidator
from django.forms import ImageField

from utils.image_utils import crop_redim_image
from .models import CustomUser
from .validators import validate_user_email

VALID_IMAGE_EXTENSIONS = [
    'bmp', 'gif', 'png', 'apng', 'jpg', 'jpeg'
]


class ImageCropField(ImageField):
    """
    Champ de formulaire permettant de rogner les images avant leur import.
    """
    default_validators = [validators.validate_image_file_extension,
                          FileExtensionValidator(allowed_extensions=VALID_IMAGE_EXTENSIONS)]


class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire de création d'utilisateur Koolapic.
    """

    email = forms.EmailField(validators=[validate_user_email])

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')


class EditProfileForm(forms.ModelForm):
    """
    Formulaire d'édition de profil.
    """

    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)
    username = forms.HiddenInput()
    profile_pic = ImageCropField(required=False, label="Image de profil")

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'tel_m',
            'tel_p',
            'npa',
            'locality',
            'address',
            'bio',
            'profile_pic',
            'x',
            'y',
            'width',
            'height',
        )

    def save(self, *args, **kwargs):
        """
        Fonction appelée à la sauvegarde du formulaire.
        Récupère les données du rognage et rogne l'image.
        """

        custom_user = super(EditProfileForm, self).save()
        if self.cleaned_data.get('width'):
            x = self.cleaned_data.get('x')
            y = self.cleaned_data.get('y')
            w = self.cleaned_data.get('width')
            h = self.cleaned_data.get('height')

            crop_redim_image((x, y, w, h), (500, 500), custom_user.profile_pic.path)

        return custom_user
