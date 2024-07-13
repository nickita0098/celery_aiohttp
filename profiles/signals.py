import asyncio

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile
from .parser import get_tasks
from .tasks import send_email_to_user

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=UserProfile)
def send_succes_message(sender, instance, created, **kwargs):
    data_for_message = {
        'subject': f'Успешная регистрация, {instance.user.username}',
        'message': f'Подтвердите свой аккаунт',
        'from_email': settings.DEFAULT_FROM_EMAIL,
        'recipient_list': [instance.user.email],
    }
    send_email_to_user.delay(data_for_message)

@receiver(post_save, sender=UserProfile)
def create_deskription(sender, instance, created, **kwargs):
    if created:
        instance.description = ', '.join(asyncio.run(
            get_tasks(
                'https://httpbin.org/delay/',
                5,
            )
        ))
        instance.save()
