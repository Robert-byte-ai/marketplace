from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from main.models import Ad
from .pagination import AdsPagination
from .permission import SellerOrReadOnly
from .serializers import AdSerializer


class AdViewSet(viewsets.ModelViewSet):
    serializer_class = AdSerializer
    pagination_class = AdsPagination
    permission_classes = (IsAuthenticated, SellerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.seller)

    def get_queryset(self, ):
        queryset = Ad.objects.all()
        if tag := self.request.query_params.get('tag'):
            queryset = queryset.filter(
                tags__contains=[tag]
            ).order_by('pk')
        return queryset
