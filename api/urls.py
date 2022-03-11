from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import AdViewSet


router_1 = DefaultRouter()

router_1.register(
    r'ads',
    AdViewSet,
    basename='api_ad'
)

urlpatterns = [
    path('', include(router_1.urls)),
    path('create/', views.obtain_auth_token),
]
