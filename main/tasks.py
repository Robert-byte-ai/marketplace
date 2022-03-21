import os
from twilio.rest import Client
import random
from dotenv import load_dotenv
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta

from main.models import Ad, Subscription, User, Seller, SMSLog
from board.celery import app

load_dotenv()


@app.task
def supper_sum(x: int, y: int) -> int:
    return x + y


@app.task
def hello() -> str:
    return 'Hello, world'


@app.task
def ads_message() -> None:
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


def send_message(message: str, emails: list) -> None:
    send_mail(
        'Notification',
        message,
        'company@gmail.com',
        emails
    )


@app.task
def send_confirmation_code(phone: int, seller_username: str) -> str:
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f'{random.randint(1000, 9999)}',
        from_=f'{os.getenv("PHONE_NUMBER")}',
        to=f'{phone}'
    )
    SMSLog.objects.create(
        seller=get_object_or_404(
            Seller,
            user__username=seller_username
        ),
        code=message.body[-4:],
        confirmed=False,
        response=message.status
    )
    return message.body[-4:]
