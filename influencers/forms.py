"""Forms for the Influencers app."""

from django import forms
from .models import BaseProfile


class ProfileForm(forms.ModelForm):
    """
    Form for creating a new profile.
    """
    class Meta:
        model = BaseProfile
        fields = ['url_profile']
        widgets = {
            'url_profile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter url profile'})
        }

