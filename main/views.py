from django.shortcuts import render
from constance import config


def index(request):
    context = {
        "turn_on_block": config.MAINTENANCE_MODE,
        "username": request.user.username
    }
    return render(request, 'index.html', context)
