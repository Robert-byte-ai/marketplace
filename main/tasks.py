import os
from twilio.rest import Client
import random
from dotenv import load_dotenv
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from main.models import Seller, SMSLog
from board.celery import app

load_dotenv()


@app.task
def supper_sum(x: int, y: int) -> int:
    return x + y


@app.task
def hello() -> str:
    return 'Hello, world'


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
