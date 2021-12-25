from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from constance import config
from django.contrib.auth import mixins
from django.db.models.signals import post_save
from django.dispatch import receiver
import random

from .tasks import ads_message
from .models import Ad, Tag, Seller, User, Subscription
from board.settings import ADS_PER_PAGE
from .forms import UserForm, ImageFormset


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
        tag = self.request.GET.get('tag')
        if tag:
            queryset = Ad.objects.filter(
                tags__name=tag
            ).order_by('pk')
        else:
            queryset = super().get_queryset()
        return queryset


class AdDetail(generic.DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad'


class SellerUpdate(mixins.LoginRequiredMixin,
                   generic.UpdateView):
    model = Seller
    fields = ('ITN',)
    template_name = 'seller_update.html'
    login_url = '/accounts/login/'
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


class AdAdd(mixins.PermissionRequiredMixin,
            mixins.LoginRequiredMixin,
            generic.CreateView, ):
    permission_required = 'main.add_ad'
    model = Ad
    fields = '__all__'
    template_name = 'ad_add.html'
    success_url = reverse_lazy("ads")
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = ImageFormset(
            self.request.POST or None,
            files=self.request.FILES or None,
            instance=self.object or None
        )
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = form.save()
            formset = self.get_context_data()['image_form']
            if formset.is_valid():
                formset.save()
            return HttpResponseRedirect(self.success_url)


class AdEdit(mixins.LoginRequiredMixin,
             generic.UpdateView):
    model = Ad
    fields = '__all__'
    template_name = 'ad_add.html'
    success_url = reverse_lazy("ads")
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = ImageFormset(
            self.request.POST or None,
            files=self.request.FILES or None,
            instance=self.object
        )
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = self.get_object()
            formset = self.get_context_data()['image_form']
            if formset.is_valid():
                formset.save()
            return HttpResponseRedirect(self.success_url)


@receiver(post_save, sender=Ad)
def ads(instance, created, **kwargs):
    if created:
        ads_message.delay([
            user.email for user in User.objects.all()
            if Subscription.objects.filter(user=user).exists()
        ])
