from django import forms
from django.forms import RadioSelect

from .models import Ad
from django.core.exceptions import ValidationError


class BordForm(forms.ModelForm):
    title = forms.CharField(min_length=15)

    class Meta:
        model = Ad
        fields = ['category', 'content',  'title', 'image']


