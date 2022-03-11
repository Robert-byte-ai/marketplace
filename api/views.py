from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from main.models import Ad
from .pagination import AdsPagination
from .serializers import AdSerializer


class AdViewSet(viewsets.ModelViewSet):
    serializer_class = AdSerializer
    permission_classes = (AllowAny,)
    pagination_class = AdsPagination

    def get_queryset(self, ):
        queryset = Ad.objects.all()
        if tag := self.request.query_params.get('tag'):
            queryset = queryset.filter(
                tags__contains=[tag]
            ).order_by('pk')
        return queryset
