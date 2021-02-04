from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.core.validators import FileExtensionValidator
from django.forms import ImageField

from utils.image_utils import crop_image
from .models import CustomUser

VALID_IMAGE_EXTENSIONS = [
    'bmp', 'gif', 'png', 'apng', 'jpg', 'jpeg'
]


class ImageCropField(ImageField):
    default_validators = [validators.validate_image_file_extension, FileExtensionValidator(allowed_extensions=VALID_IMAGE_EXTENSIONS)]


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')


class CustomUserChangeForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)
    profile_pic = ImageCropField(required=False, label="Photo de profil")

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'tel_m', 'tel_p', 'npa', 'locality', 'address', 'bio', 'profile_pic', 'x', 'y', 'width', 'height')

    def save(self, *args, **kwargs):
        custom_user = super(CustomUserChangeForm, self).save()
        if self.cleaned_data.get('width'):
            x = self.cleaned_data.get('x')
            y = self.cleaned_data.get('y')
            w = self.cleaned_data.get('width')
            h = self.cleaned_data.get('height')

            crop_image((x, y, w, h), (500, 500), custom_user.profile_pic.path)

        return custom_user
