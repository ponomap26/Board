from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

from brd.models import Author


class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    username = forms.CharField(required=True, max_length=15, label='Логин', min_length=2)
    password1 = forms.CharField(required=True, max_length=30, label='Пароль', min_length=8)
    password2 = forms.CharField(required=True, max_length=30, label='Повторите пароль')
    error_messages = {
        'password_mismatch': ("Пароли не совпадают."),
        'error': ("Форма не валидна."),
        'username_exists': ("Пользователь с таким именем уже существует."),
    }

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2')

    def save(self, request):
        user = super().save(request)

        common_users = Group.objects.get(name="author")
        Author.objects.create(authorUser=User.objects.get(pk=user.id))
        user.groups.add(common_users)
        return user


class MyActivationCodeForm(forms.Form):
    error_css_class = 'has-error'
    error_messages = {'password_incorrect':
                          ("Старый пароль не верный. Попробуйте еще раз."),
                      'password_mismatch':
                          ("Пароли не совпадают."),
                      'cod-no':
                          ("Код не совпадает."), }

    def __init__(self, *args, **kwargs):
        super(MyActivationCodeForm, self).__init__(*args, **kwargs)

    code = forms.CharField(required=True, max_length=50, label='Код подтвержения',
                           widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                           error_messages={'required': 'Введите код!',
                                           'max_length': 'Максимальное количество символов 50'})

    def save(self, commit=True):
        profile = super(MyActivationCodeForm, self).save(commit=False)
        profile.code = self.cleaned_data['code']

        if commit:
            profile.save()
        return profile
