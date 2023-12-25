from django import forms
from .models import BaseProfile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = BaseProfile
        fields = ['url_profile']
        widgets = {
            'url_profile': forms.URLInput(attrs={'class': 'form-control'}),

        }

