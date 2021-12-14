from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from django.contrib.flatpages.models import FlatPage

from .models import Seller, Category, Tag, Ad, ArchiveAds, Picture


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


class PictureAdmin(admin.ModelAdmin):
    list_display = ["ad"]


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(ArchiveAds)
admin.site.register(Picture, PictureAdmin)
