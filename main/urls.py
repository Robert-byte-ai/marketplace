from django.urls import path, include

from . import views

urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("", views.index, name="index"),
]
