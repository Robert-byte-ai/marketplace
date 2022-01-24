from django.core.mail import send_mail

from board.celery import app


@app.task
def supper_sum(x, y):
    return x + y


@app.task
def hello():
    return 'Hello, world'


@app.task
def ads_message(emails):
    return send_mail(
        'Notification',
        'New ad',
        'company@gmail.com',
        emails
    )
