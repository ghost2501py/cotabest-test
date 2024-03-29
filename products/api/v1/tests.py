from rest_framework import status
from snapshottest.django import TestCase

from django.test import Client
from django.urls import reverse

from ...models import Product


class ProductListTest(TestCase):
    def setUp(self):
        self.client = Client()
        Product.objects.create(
            name='Ração para coelho',
            price=30.00,
            minimun=2,
            amount_per_package=2,
            max_availability=70000,
        )
        Product.objects.create(
            name='Ração para gato',
            price=50.00,
            minimun=40,
            amount_per_package=7,
            max_availability=50000,
        )
        Product.objects.create(
            name='Pão de forma',
            price=4.50,
            minimun=200,
            amount_per_package=20,
            max_availability=400000,
        )

    def test_get_all_products(self):
        response = self.client.get(reverse('api_v1:products:product-list'))
        self.assertMatchSnapshot(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_products_by_name(self):
        url = reverse('api_v1:products:product-list') + '?name=açã'
        response = self.client.get(url)
        self.assertMatchSnapshot(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
