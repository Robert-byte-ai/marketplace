from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from constance import config
from django.contrib.auth import mixins
import random

from .models import Ad, Tag, Seller
from board.settings import ADS_PER_PAGE
from .forms import UserForm


def index(request):
    context = {
        "turn_on_block": config.MAINTENANCE_MODE,
        'notifications': random.randint(0, 100),
        'hello': 'Привет, мир!'
    }
    return render(request, 'index.html', context)


class AdList(generic.ListView):
    queryset = Ad.objects.all().order_by('pk')
    paginate_by = ADS_PER_PAGE
    template_name = 'ad_list.html'
    context_object_name = 'ads_list'
    extra_context = {
        'tags': Tag.objects.all(),
        'notifications': random.randint(0, 100),
        'hello': 'Привет, мир!'
    }

    def get_queryset(self):
        return Ad.objects.filter(
            tags__name=self.request.GET.get('tag')
        )


class AdDetail(generic.DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad'


class SellerUpdate(mixins.LoginRequiredMixin,
                   generic.UpdateView):
    model = Seller
    fields = ('ITN',)
    template_name = 'seller_update.html'
    login_url = 'ads'
    success_url = reverse_lazy("seller_update")

    def get_object(self, queryset=None):
        return get_object_or_404(
            Seller,
            user=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserForm(
            self.request.POST or None,
            instance=self.request.user
        )
        return context

    def form_valid(self, form):
        user_form = self.get_context_data()['user_form']
        if user_form.is_valid():
            user_form.save()
        return super().form_valid(form)


class AdAdd(mixins.LoginRequiredMixin,
            generic.CreateView):
    model = Ad
    fields = '__all__'
    template_name = 'ad_add.html'
    success_url = reverse_lazy("ads")
    login_url = 'ads'


class AdEdit(mixins.LoginRequiredMixin,
             generic.UpdateView):
    model = Ad
    fields = '__all__'
    template_name = 'ad_add.html'
    success_url = reverse_lazy("ads")
    login_url = 'ads'
