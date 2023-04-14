from django import forms
from django.forms import RadioSelect

from .models import Ad, Response
from django.core.exceptions import ValidationError


class BordForm(forms.ModelForm):
    title = forms.CharField(min_length=15)

    class Meta:
        model = Ad
        fields = ['category', 'content', 'title', 'image']


class ResponseForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = Response
        fields = ['content']


class BlogsDelete(forms.ModelForm):
    class Meta:
        model = Ad
        fields = []


class BlogsEdit(forms.ModelForm):
    title = forms.CharField(min_length=15)

    class Meta:
        model = Ad
        fields = ['category', 'title', 'content', 'image']


class ResponseForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Response
        fields = ('text',)
        labels = {'text': 'Комментарий'}
        widgets = {'text': forms.Textarea}

    def save(self, commit=True):
        response = super().save(commit=False)
        if commit:
            response.post = self.instance.post
            response.save()
        return response