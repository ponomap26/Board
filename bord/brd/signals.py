from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.signals import request_finished
from django.template.loader import render_to_string

from django.urls import reverse
from django.utils.html import strip_tags

from .models import Response

from django.db.models.signals import post_save, m2m_changed, pre_save

from django.core.mail import send_mail

from django.dispatch import receiver

from .views import accept_response, add_response

#
# request_finished.connect(add_response)


@receiver(post_save, sender=Response)
def send_notification_email(sender, instance, created, **kwargs):
    if created:
        ad = instance.ad
        subject = 'Новый отзыв на объявление "{}"'.format(ad.title)
        message = render_to_string('notification_email.html', {
            'ad': ad,
            'response': instance,
            'domain': get_current_site(None).domain,
            'url': reverse('response_detail', args=[ad.pk])
        })
        from_email = 'noreply@example.com'
        recipient_list = [ad.author.email]
        send_mail(subject, message, from_email, recipient_list)


@receiver(m2m_changed, sender=Response)
def accept_response_signal(sender, instance, **kwargs):
    if instance.accepted:

        return
    print("Accepted")
    instance.accepted = True
    instance.save()

    # Отправка сообщения на email автора отзыва
    subject = 'Ваш отзыв принят'

    message = render_to_string('response_accepted.html', {



    })
    from_email = 'noreply@example.com'
    recipient_list = [instance.author.email]
    send_mail(subject, message, from_email, recipient_list)
