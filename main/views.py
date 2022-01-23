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


class SellerUpdateView(mixins.LoginRequiredMixin,
                       generic.UpdateView):
    template_name = 'seller_update.html'
    model = Seller
    form_class = SellerForm
    success_url = reverse_lazy("seller_update")

    def get_object(self, queryset=None):
        seller, created = Seller.objects.get_or_create(user=self.request.user)
        return seller

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if 'user_form' not in context:
            context['user_form'] = UserForm(instance=user)
        if 'confirmation_form' not in context:
            sms = SMSLog.objects.filter(seller=self.object)
            if sms and not sms.get().confirmed:
                context['confirmation_form'] = CodeForm()
        return context

    def form_valid(self, form):
        self.object = form.save()
        if 'phone' in form.changed_data:
            send_confirmation_code.delay(
                self.request.POST.get('phone'),
                self.object.user.username
            )
        all_forms_are_valid = True
        forms_context = {'form': form}
        user = User.objects.get(seller=self.object)
        user_form = UserForm(self.request.POST, instance=user)
        forms_context['user_form'] = user_form
        if user_form.is_valid():
            user_form.save()
        else:
            all_forms_are_valid = False
        sms = SMSLog.objects.filter(seller=self.object)
        if sms and not (sms_log := sms.get()).confirmed:
            confirmation_form = CodeForm(self.request.POST)
            forms_context['confirmation_form'] = confirmation_form
            if confirmation_form.is_valid():
                confirmation_code = confirmation_form.cleaned_data['code']
                if confirmation_code == sms_log.code:
                    sms_log.confirmed = True
                    sms_log.save()
                else:
                    confirmation_form.add_error(
                        field='confirmation_code',
                        error=ValidationError(
                            'Ошибочный код подтверждения: %(value)s',
                            code='invalid',
                            params={'value': confirmation_code},
                        )
                    )
                    all_forms_are_valid = False
            else:
                all_forms_are_valid = False
        if all_forms_are_valid:
            return HttpResponseRedirect(self.get_success_url())
        else:
            self.render_to_response(self.get_context_data(
                    form=form,
                    user_form=user_form,
                    **forms_context,
                )
            )


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
