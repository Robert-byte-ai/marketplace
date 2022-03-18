from rest_framework.pagination import PageNumberPagination


class AdsPagination(PageNumberPagination):
    page_size = 5
