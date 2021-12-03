from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from django.contrib.flatpages.models import FlatPage


class FlatPageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        fields = '__all__'


class FlatPageAdmin(admin.ModelAdmin):
    form = FlatPageAdminForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
