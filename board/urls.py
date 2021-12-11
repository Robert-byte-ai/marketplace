from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('pages/', include('django.contrib.flatpages.urls')),
    path('admin/', admin.site.urls),
    path("", include("main.urls")),
]
