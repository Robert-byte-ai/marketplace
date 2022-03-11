from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from main.models import Ad
from .serializers import AdSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (AllowAny,)

