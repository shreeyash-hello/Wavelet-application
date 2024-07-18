from django import forms
from .models import UploadedImage


class UploadImageForm(forms.ModelForm):
    OPERATION_CHOICES = [
        ('encrypt', 'Encrypt Image'),
        ('compress', 'Compress Image'),
    ]

    operation = forms.ChoiceField(choices=OPERATION_CHOICES, required=True)

    class Meta:
        model = UploadedImage
        fields = ['image', 'operation']
