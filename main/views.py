from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from constance import config
from django.contrib.auth import mixins
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import random

<<<<<<<<< Temporary merge branch 1
from .models import Ad, Tag, Seller, SMSLog, Group
=========
from .models import Ad, Tag, Seller, SMSLog, User
>>>>>>>>> Temporary merge branch 2
from board.settings import ADS_PER_PAGE
from .forms import UserForm, ImageFormset, CodeForm, SellerForm
from .tasks import send_confirmation_code


def index(request):
    context = {
        "turn_on_block": config.MAINTENANCE_MODE,
        'notifications': random.randint(0, 100),
        'hello': 'Привет, мир!'
    }
    return render(request, 'index.html', context)


@method_decorator(cache_page(60 * 5), name='dispatch')
class AdList(generic.ListView):
    queryset = Ad.objects.all()
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
            )
        else:
            queryset = super().get_queryset()
        return queryset.order_by('pk')


class AdDetail(generic.DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        if cache.get('new_price') is None:
            cache.set(
                'new_price',
                self.object.price * random.uniform(0.8, 1.2),
                60
            )
        context = super().get_context_data(**kwargs)
        context['new_price'] = cache.get('new_price')
        return context


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

<<<<<<<<< Temporary merge branch 1
    def save_forms(self, user_form, form):
        if user_form.is_valid() and form.is_valid():
            return user_form.save(), form.save()

    def post(self, request, *args, **kwargs):
        phone = self.request.POST.get('phone')
        self.object = self.get_object()
        form = self.get_form()
        user_form = self.get_context_data()['user_form']
        if self.object.phone == phone:
            self.save_forms(user_form, form)
            return HttpResponseRedirect(self.success_url)
        elif self.object.phone != phone:
=========
    def form_valid(self, form):
        self.object = form.save()
        if 'phone' in form.changed_data:
>>>>>>>>> Temporary merge branch 2
            send_confirmation_code.delay(
                self.request.POST.get('phone'),
                self.object.user.username
            )
<<<<<<<<< Temporary merge branch 1
            self.save_forms(user_form, form)
            return HttpResponseRedirect(self.message_url)


class VerifyCode(mixins.LoginRequiredMixin,
                 generic.TemplateView):
    success_url = reverse_lazy('seller_update')
    template_name = 'verify_phone.html'

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
=========
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
>>>>>>>>> Temporary merge branch 2


class AdAdd(mixins.LoginRequiredMixin,
            generic.CreateView, ):
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
        if 'banned_users' in [group.name for group in request.user.groups.all()]:
            return HttpResponseBadRequest('You are banned')
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
