from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from constance import config
from django.contrib.auth import mixins
import random

from .models import Ad, Tag, Seller, SMSLog
from board.settings import ADS_PER_PAGE
from .forms import UserForm, ImageFormset, CodeForm
from .tasks import send_confirmation_code


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
    fields = ('ITN', 'phone')
    template_name = 'seller_update.html'
    login_url = '/accounts/login/'
    success_url = reverse_lazy("seller_update")
    message_url = '/accounts/seller/message'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Seller,
            user=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserForm(
            self.request.POST or None,
            instance=self.object.user
        )
        return context

    def post(self, request, *args, **kwargs):
        phone = self.request.POST.get('phone')
        self.object = self.get_object()
        form = self.get_form()
        user_form = self.get_context_data()['user_form']
        if self.object.phone != phone and form.is_valid():
            form.save()
            send_confirmation_code.delay(
                phone, self.request.user.username
            )
            return HttpResponseRedirect(self.message_url)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(self.success_url)


class VerifyCode(mixins.PermissionRequiredMixin,
                 mixins.LoginRequiredMixin,
                 generic.TemplateView):
    success_url = reverse_lazy('seller_update')
    template_name = 'verify_phone.html'
    permission_required = 'main.seller_message'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['code_form'] = CodeForm(
            self.request.POST or None,
        )
        return context

    def post(self, request, *args, **kwargs):
        if get_object_or_404(
                SMSLog,
                seller__user=self.request.user
        ).code == request.POST.get('code'):
            return HttpResponseRedirect(self.success_url)
        return HttpResponseBadRequest('Wrong confirmation code')


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
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.save()
            formset = self.get_context_data()['image_form']
            if formset.is_valid():
                formset.save()
            return HttpResponseRedirect(self.success_url)
