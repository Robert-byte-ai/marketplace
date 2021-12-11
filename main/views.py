from django.shortcuts import render, get_object_or_404
from django.views import generic
from constance import config
import random

from .models import Ad, Tag
from board.settings import ADS_PER_PAGE


def index(request):
    context = {
        "turn_on_block": config.MAINTENANCE_MODE,
        "username": request.user.username,
        'notifications': random.randint(0, 100),
        'hello': 'Привет, мир!'
    }
    return render(request, 'index.html', context)


class AdList(generic.ListView):
    queryset = Ad.objects.all().order_by('pk')
    paginate_by = ADS_PER_PAGE
    template_name = 'ad_list.html'
    context_object_name = 'ads_list'
    extra_context = {'tags': Tag.objects.all()}

    def get_queryset(self):
        return Ad.objects.filter(tags__name=self.request.GET.get('tag'))


class AdDetail(generic.DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad'
