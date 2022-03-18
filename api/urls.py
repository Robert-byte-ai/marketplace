from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi

from .views import AdViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="MarketPlace",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

swagger_urls = [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0)
        , name='schema-json'
    ),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]

router_1 = DefaultRouter()

router_1.register(
    r'ads',
    AdViewSet,
    basename='api_ad'
)

urlpatterns = [
    path('', include(router_1.urls)),
    path('create/', views.obtain_auth_token),
    path('', include(swagger_urls))
]
