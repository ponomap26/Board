import random
from email.headerregistry import Group

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from accounts.forms import CustomSignupForm, MyActivationCodeForm
from brd.models import Profile


def generate_code():
    random.seed()
    return str(random.randint(10000, 99999))





def register(request):
    if not request.user.is_authenticated:
        if request.POST:
            form = CustomSignupForm(request.POST or None)
            if form.is_valid():
                # Создаем пользователя
                user = form.save(request)
                # Устанавливаем is_active в False, чтобы активировать аккаунт
                user.is_active = False
                user.save()
                # Генерируем случайный код активации
                code = generate_code()
                # Сохраняем код активации в профиле пользователя
                profile = Profile(user=user, code=code)
                profile.save()
                # Отправляем код активации пользователю по электронной почте
                message = f"Ваш код активации: {code}"
                send_mail('Код активации', message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                # Добавляем пользователя в группу authors
                # user.groups.add(Group.objects.get(name='authors'))
                # Завершаем регистрацию и перенаправляем пользователя на страницу ввода кода активации
                return redirect('accounts:activation_code')
            else:
                return render(request, 'registration/signup.html', {'form': form})
        else:
            return render(request, 'registration/signup.html', {'form': CustomSignupForm})
    else:
        return redirect('accounts:activation_code')

def endreg(request):
    if request.user.is_authenticated:
        return redirect('/blogs/')
    else:
        if request.method == 'POST':
            form = MyActivationCodeForm(request.POST)
            if form.is_valid():
                # Получаем отправленный код активации
                code_use = form.cleaned_data.get("code")
                # Получаем профиль пользователя по коду активации
                try:
                    profile = Profile.objects.get(code=code_use)
                except Profile.DoesNotExist:
                    form.add_error(None, "Код подтверждения не совпадает.")
                    return render(request, 'activation_code', {'form': form})
                # Если аккаунт еще не активирован
                if not profile.user.is_active:
                    # Активируем аккаунт и сохраняем изменения
                    profile.user.is_active = True
                    profile.user.save()
                    # Авторизуем пользователя
                    user = authenticate(username=profile.user.username, password=profile.user.password)
                    login(request, profile.user, backend='django.contrib.auth.backends.ModelBackend')
                    # Удаляем пользователя и профиль
                    # profile.user.delete()
                    # Перенаправляем на главную страницу
                    return redirect('/blogs/')
                else:
                    form.add_error(None, 'Аккаунт уже активирован')

                    return render(request, 'registration/activation_code.html', {'form': form})
            else:
                return render(request, 'registration/activation_code.html', {'form': form})
        else:
            form = MyActivationCodeForm()
            return render(request, 'registration/activation_code.html', {'form': form})