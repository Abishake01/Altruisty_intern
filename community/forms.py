from django import forms
from PIL import Image
from django.core.exceptions import ValidationError

# Custom validator to check image size
def validate_image_size(image):
    try:
        img = Image.open(image)
        width, height = img.size
        if width != 250 or height != 250:
            raise ValidationError("Image must be 250x250 pixels.")
    except Exception as e:
        raise ValidationError("Invalid image file.")

class create_communityf(forms.Form):
    community_name = forms.CharField(max_length='30')
    community_profile = forms.FileField(required=True, validators=[validate_image_size],widget=forms.ClearableFileInput(attrs={'placeholder': 'Upload community profile image'}))

class edit_profilef(forms.Form):
    Bio = forms.CharField(max_length='30')
    Profile = forms.FileField(required=True, validators=[validate_image_size],widget=forms.ClearableFileInput(attrs={'placeholder': 'Upload community profile image'}))

class change_communityf(forms.Form):
    Updated_community_name = forms.CharField(max_length='30')
    Updated_community_profile = forms.FileField(required=True, validators=[validate_image_size],widget=forms.ClearableFileInput(attrs={'placeholder': 'Upload community profile image'}))
    