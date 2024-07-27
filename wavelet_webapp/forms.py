from django import forms
from .models import UploadedImage
from django.core.exceptions import ValidationError

class UploadImageForm(forms.ModelForm):
    OPERATION_CHOICES = [
        ('encrypt', 'Encrypt Image'),
        ('compress', 'Compress Image'),
    ]

    operation = forms.ChoiceField(choices=OPERATION_CHOICES, required=True)

    class Meta:
        model = UploadedImage
        fields = ['image', 'operation']

