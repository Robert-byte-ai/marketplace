from django.core.management.base import BaseCommand

from main.factories import (
    UserFactory,
    SellerFactory,
    TagFactory,
    CategoryFactory,
    AdFactory
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for i in range(10):
            UserFactory(),
            SellerFactory(),
            TagFactory(),
            CategoryFactory(),
            AdFactory()
