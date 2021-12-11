from django.urls import path, include

from . import views

urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("", views.index, name="index"),
    path('ads/', views.AdList.as_view(), name='ads'),
    path('ads/<int:pk>', views.AdDetail.as_view(), name='ad')
]
