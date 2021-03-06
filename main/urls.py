from django.urls import path, include
from django.contrib.sitemaps.views import sitemap

from . import views
from .sitemaps import AdSitemap

sitemaps = {
    'ad': AdSitemap,
}

urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', views.index, name="index"),
    path('ads/', views.AdList.as_view(), name='ads'),
    path('ads/<int:pk>', views.AdDetail.as_view(), name='ad'),
    path('accounts/seller', views.SellerUpdateView.as_view(), name='seller_update'),
    path('ads/add', views.AdAdd.as_view(), name='ad_add'),
    path('ads/<int:pk>/edit', views.AdEdit.as_view(), name='ad_edit'),
    path('robots.txt', views.robots_txt),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')

]
