from django.urls import path, include

from . import views

urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("", views.index, name="index"),
    path('ads/', views.AdList.as_view(), name='ads'),
    path('ads/<int:pk>', views.AdDetail.as_view(), name='ad'),
    path('accounts/seller', views.SellerUpdate.as_view(), name='seller_update'),
    path('accounts/seller/message', views.VerifyCode.as_view(), name='seller_phone'),
    path('ads/add', views.AdAdd.as_view(), name='ad_add'),
    path('ads/<int:pk>/edit', views.AdEdit.as_view(), name='ad_edit'),

]
