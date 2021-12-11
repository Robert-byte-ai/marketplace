from django.shortcuts import render
from constance import config
import random


def index(request):
    context = {
        "turn_on_block": config.MAINTENANCE_MODE,
        "username": request.user.username,
        'notifications': random.randint(0, 100),
        'hello': 'Привет, мир!'
    }
    return render(request, 'index.html', context)
