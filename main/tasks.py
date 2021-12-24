from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from board.celery import app
from .models import Ad, Subscription, User


@app.task
def supper_sum(x, y):
    return x + y


@app.task
def hello():
    return 'Hello, world'


@receiver(post_save, sender=Ad)
def new_ads(instance, created, **kwargs):
    if created:
        send_mail(
            'Notification',
            f'New ad: {instance}',
            'company@gmail.com',
            [
                user.email for user in User.objects.all()
                if Subscription.objects.filter(user=user).exists()
            ]
        )


@app.task
def ads_message():
    return new_ads

