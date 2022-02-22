import factory
import random

from .models import (
    User,
    Seller,
    Category,
    Ad
)


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(
        lambda n: 'test-user{}'.format(n)
    )
    email = factory.LazyAttribute(
        lambda a: '{}@example.com'.format(a.username).lower()
    )
    password = factory.Faker('password')

    class Meta:
        model = User
        django_get_or_create = (
            'username',
            'email',
            'password'
        )


class SellerFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Seller
        django_get_or_create = ('user',)


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Faker(
        'sentence',
        nb_words=5,
        variable_nb_words=True
    )

    class Meta:
        model = Category
        django_get_or_create = ('name',)


class AdFactory(factory.django.DjangoModelFactory):
    name = factory.Faker(
        'sentence',
        nb_words=5,
        variable_nb_words=True
    )
    category = factory.SubFactory(CategoryFactory)
    seller = factory.SubFactory(SellerFactory)
    price = factory.LazyAttribute(
        lambda a: random.randint(0, 10000)
    )

    class Meta:
        model = Ad
        django_get_or_create = (
            'name',
            'category',
            'seller',
            'price'
        )

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
