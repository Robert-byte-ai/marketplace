from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from django.contrib.flatpages.models import FlatPage
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import (
    Seller,
    Category,
    Ad,
    ArchiveAds,
    Picture,
    Subscription,
    SMSLog
)


class FlatPageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        fields = '__all__'


class FlatPageAdmin(admin.ModelAdmin):
    form = FlatPageAdminForm


class SellerAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", 'count_ads', 'ITN',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)


def archive(modeladmin, request: HttpRequest, queryset: QuerySet) -> None:
    queryset.update(is_archive=True)


class AdAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'seller',
        'pub_date',
        'edited_date',
        'price',
        'pk',
    )
    list_filter = ('tags', 'pub_date')
    actions = [archive]


class PictureAdmin(admin.ModelAdmin):
    list_display = ["ad"]


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(Tag, TagAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(ArchiveAds)
admin.site.register(SMSLog)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Subscription)
