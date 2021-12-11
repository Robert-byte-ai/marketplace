from django.shortcuts import render
from django.views import generic
from constance import config
import random

from .models import Ad


def index(request):
    context = {
        "turn_on_block": config.MAINTENANCE_MODE,
        "username": request.user.username,
        'notifications': random.randint(0, 100),
        'hello': 'Привет, мир!'
    }
    return render(request, 'index.html', context)


class AdList(generic.ListView):
    model = Ad
    template_name = 'ad_list.html'
    context_object_name = 'ads_list'


class AdDetail(generic.DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad'
