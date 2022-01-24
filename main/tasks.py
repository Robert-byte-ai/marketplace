from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

from main.models import Ad, Subscription, User
from board.celery import app


@app.task
def supper_sum(x, y):
    return x + y


@app.task
def hello():
    return 'Hello, world'


@app.task
def ads_message():
    ads_for_week = Ad.objects.filter(
        pub_date__range=(
            (timezone.now() - timedelta(days=7)),
            timezone.now()
        )
    )
    emails = [
        user.email for user in User.objects.all()
        if Subscription.objects.filter(user=user).exists()
    ]
    ads = [ad.name for ad in ads_for_week]
    if len(ads_for_week) > 0:
        return send_message(f'New ads: {" ".join(ads)}', emails)
    return send_message('There are no ads', emails)


def send_message(message, emails):
    send_mail(
        'Notification',
        message,
        'company@gmail.com',
        emails
    )
