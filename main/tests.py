from django.test import TestCase, Client
from django.urls import reverse
import pytest

from .models import Category, User, Ad, Seller, Group

HOME_URL = reverse('index')

ADS_URL = reverse('ads')

USERNAME = 'Robert'

SELLER_UPDATE_URL = reverse('seller_update')

PHONE_CONFIRM_URL = reverse('seller_phone')

AD_ADD_URL = reverse('ad_add')


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(name='common_users')
        cls.user = User.objects.create_user(username=USERNAME)
        cls.seller = Seller.objects.create(user=cls.user, avatar=None)
        cls.category = Category.objects.create(name='Тестовая категория')
        cls.ad = Ad.objects.create(
            name='Текст',
            category=cls.category,
            seller=cls.seller
        )
        cls.AD_EDIT_URL = reverse('ad_edit', kwargs={
            'pk': cls.ad.pk
        })
        cls.AD_URL = reverse('ad', kwargs={
            'pk': cls.ad.pk
        })

        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_url_status(self):
        test_urls = [
            [HOME_URL, self.guest_client, 200],
            [ADS_URL, self.guest_client, 200],
            [SELLER_UPDATE_URL, self.authorized_client, 200],
            [PHONE_CONFIRM_URL, self.authorized_client, 200],
            [AD_ADD_URL, self.authorized_client, 200],
            [self.AD_EDIT_URL, self.authorized_client, 200],
            [self.AD_URL, self.guest_client, 200],
        ]
        for url, client, status in test_urls:
            with self.subTest(url=url, client=client):
                self.assertEqual(client.get(url).status_code, status)


@pytest.fixture
def setUp():
    Group.objects.create(name='common_users')
    user = User.objects.create_user(username=USERNAME)
    seller = Seller.objects.create(user=user, avatar=None)
    category = Category.objects.create(name='Тестовая категория')
    ad = Ad.objects.create(
        name='Текст',
        category=category,
        seller=seller
    )
    AD_EDIT_URL = reverse('ad_edit', kwargs={
        'pk': ad.pk
    })
    AD_URL = reverse('ad', kwargs={
        'pk': ad.pk
    })

    guest_client = Client()
    authorized_client = Client()
    authorized_client.force_login(user)
    return {
        'AD_EDIT_URL': AD_EDIT_URL,
        'AD_URL': AD_URL,
        'guest_client': guest_client,
        'authorized_client': authorized_client,
    }


@pytest.mark.django_db
def test_url_status(setUp):
    test_urls = [
        [HOME_URL, setUp['guest_client'], 200],
        [ADS_URL, setUp['guest_client'], 200],
        [SELLER_UPDATE_URL, setUp['authorized_client'], 200],
        [PHONE_CONFIRM_URL, setUp['authorized_client'], 200],
        [AD_ADD_URL, setUp['authorized_client'], 200],
        [setUp['AD_EDIT_URL'], setUp['authorized_client'], 200],
        [setUp['AD_EDIT_URL'], setUp['authorized_client'], 200],
    ]
    for url, client, status in test_urls:
        assert client.get(url).status_code == status
