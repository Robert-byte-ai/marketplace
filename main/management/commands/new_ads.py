from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

from main.models import Ad, Subscription, User

scheduler = BackgroundScheduler(timezone='Europe/Moscow')


def ads():
    if Ad.objects.latest('pub_date').pub_date.date() > (
            datetime.today().date() - timedelta(days=7)
    ):
        send_mail(
            'Notification',
            f'New ads',
            'company@gmail.com',
            [
                user.email for user in User.objects.all()
                if Subscription.objects.filter(user=user).exists()
            ]
        )


class Command(BaseCommand):

    def handle(self, *args, **options):
        scheduler.add_job(func=ads, trigger='interval', weeks=1)
        scheduler.start()
