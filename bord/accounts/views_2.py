from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from .forms import CustomSignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from django.core.mail import EmailMessage

from .token import account_activation_token


def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Ссылка для активации была отправлена на ваш электронный адрес'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Пожалуйста, подтвердите свой адрес электронной почты, чтобы завершить регистрацию')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Это электронная почта уже зарегистрировано.')
                form.add_error('email', 'Это электронная почта уже зарегистрировано.')
            else:
                form.save()
                messages.success(request, 'Ваша учетная запись была создана.')
                return redirect('home')

    else:
        form = CustomSignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse(
            'Благодарим вас за подтверждение по электронной почте. Теперь вы можете войти в свою учетную запись.')
    else:
        return HttpResponse('Ссылка для активации недействительна!')
