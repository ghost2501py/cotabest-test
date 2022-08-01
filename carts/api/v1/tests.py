from decimal import Decimal
import json

from rest_framework import status
from snapshottest.django import TestCase

from django.test import Client
from django.urls import reverse

from orders.models import Order
from products.models import Product
from products.api.v1.serializers import ProductSerializer
from ...models import Cart, CartItem
from .serializers import CartSerializer

client = Client()


class CartsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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

    def test_create_cart(self):
        carts_count = Cart.objects.count()
        response = client.post(reverse('api_v1:carts:cart-create'))
        cart = Cart.objects.all().last()
        self.assertEqual(Cart.objects.count(), carts_count + 1)
        self.assertMatchSnapshot(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_product(self):
        cart = Cart.objects.create()
        cart_items_count = cart.cartitem_set.count()
        product = Product.objects.all().first()
        response = client.post(
            reverse('api_v1:carts:add-product', kwargs={'pk': cart.pk}),
            data=json.dumps({'product_pk': product.pk, 'quantity': 4}),
            content_type='application/json',
        )
        cart.refresh_from_db()
        self.assertEqual(cart.cartitem_set.count(), cart_items_count + 1)
        self.assertMatchSnapshot(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO: test model instance

    def test_detail(self):
        cart = Cart.objects.create()
        product = Product.objects.all().first()
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=4)
        response = client.get(reverse('api_v1:carts:cart-detail', kwargs={'pk': cart.pk}))
        self.assertMatchSnapshot(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_product_quantity(self):
        cart = Cart.objects.create()
        product = Product.objects.all().first()
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=4)
        response = client.put(
            reverse('api_v1:carts:change-quantity', kwargs={'pk': cart.pk}),
            data=json.dumps({'product_pk': product.pk, 'quantity': 6}),
            content_type='application/json',
        )
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 6)
        self.assertMatchSnapshot(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_product(self):
        cart = Cart.objects.create()
        product = Product.objects.all().first()
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=4)
        response = client.delete(
            reverse('api_v1:carts:remove-product', kwargs={'pk': cart.pk, 'product_pk': product.pk}),
            content_type='application/json',
        )
        self.assertRaises(CartItem.DoesNotExist, cart_item.refresh_from_db)
        self.assertMatchSnapshot(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_finish(self):
        cart = Cart.objects.create()
        product = Product.objects.all().first()
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=4)
        orders_count = Order.objects.count()
        response = client.post(reverse('api_v1:carts:finish', kwargs={'pk': cart.pk}))
        # TODO: test if UUID is valid
        response.data['id'] = '(uuid removed)'
        self.assertMatchSnapshot(response.data)
        cart.refresh_from_db()
        self.assertEqual(cart.cartitem_set.count(), 0)
        self.assertEqual(Order.objects.count(), orders_count + 1)
        self.assertEqual(cart.total_price, Decimal("0.00"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO: test Order model instance

    def test_add_product_error_quantity_incompatible(self):
        cart = Cart.objects.create()
        cart_items_count = cart.cartitem_set.count()
        product = Product.objects.all().first()
        response = client.post(
            reverse('api_v1:carts:add-product', kwargs={'pk': cart.pk}),
            data=json.dumps({'product_pk': product.pk, 'quantity': 5}),
            content_type='application/json',
        )
        cart.refresh_from_db()
        self.assertEqual(cart.cartitem_set.count(), cart_items_count)
        self.assertMatchSnapshot(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_product_error_quantity_less_than_minimun(self):
        cart = Cart.objects.create()
        cart_items_count = cart.cartitem_set.count()
        product = Product.objects.all().last()
        response = client.post(
            reverse('api_v1:carts:add-product', kwargs={'pk': cart.pk}),
            data=json.dumps({'product_pk': product.pk, 'quantity': 20}),
            content_type='application/json',
        )
        cart.refresh_from_db()
        self.assertEqual(cart.cartitem_set.count(), cart_items_count)
        self.assertMatchSnapshot(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_product_error_quantity_greater_than_max_availability(self):
        cart = Cart.objects.create()
        cart_items_count = cart.cartitem_set.count()
        product = Product.objects.all().first()
        response = client.post(
            reverse('api_v1:carts:add-product', kwargs={'pk': cart.pk}),
            data=json.dumps({'product_pk': product.pk, 'quantity': 70002}),
            content_type='application/json',
        )
        cart.refresh_from_db()
        self.assertEqual(cart.cartitem_set.count(), cart_items_count)
        self.assertMatchSnapshot(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_product_error_already_in_cart(self):
        cart = Cart.objects.create()
        product = Product.objects.all().first()
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=4)
        cart_items_count = cart.cartitem_set.count()
        response = client.post(
            reverse('api_v1:carts:add-product', kwargs={'pk': cart.pk}),
            data=json.dumps({'product_pk': product.pk, 'quantity': 4}),
            content_type='application/json',
        )
        cart.refresh_from_db()
        self.assertMatchSnapshot(json.dumps(response.data))
        self.assertEqual(cart.cartitem_set.count(), cart_items_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_quantity_error_quantity_incompatible(self):
        cart = Cart.objects.create()
        product = Product.objects.all().first()
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=4)
        response = client.put(
            reverse('api_v1:carts:change-quantity', kwargs={'pk': cart.pk}),
            data=json.dumps({'product_pk': product.pk, 'quantity': 5}),
            content_type='application/json',
        )
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 4)
        self.assertMatchSnapshot(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_quantity_error_quantity_less_than_minimun(self):
        cart = Cart.objects.create()
        product = Product.objects.all().last()
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=200)
        response = client.put(
            reverse('api_v1:carts:change-quantity', kwargs={'pk': cart.pk}),
            data=json.dumps({'product_pk': product.pk, 'quantity': 20}),
            content_type='application/json',
        )
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 200)
        self.assertMatchSnapshot(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_quantity_error_quantity_greater_than_max_availability(self):
        cart = Cart.objects.create()
        product = Product.objects.all().first()
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=4)
        response = client.put(
            reverse('api_v1:carts:change-quantity', kwargs={'pk': cart.pk}),
            data=json.dumps({'product_pk': product.pk, 'quantity': 70002}),
            content_type='application/json',
        )
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 4)
        self.assertMatchSnapshot(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_quantity_error_not_in_cart(self):
        cart = Cart.objects.create()
        product = Product.objects.all().first()
        cart_items_count = cart.cartitem_set.count()
        response = client.put(
            reverse('api_v1:carts:change-quantity', kwargs={'pk': cart.pk}),
            data=json.dumps({'product_pk': product.pk, 'quantity': 4}),
            content_type='application/json',
        )
        cart.refresh_from_db()
        self.assertMatchSnapshot(json.dumps(response.data))
        self.assertEqual(cart.cartitem_set.count(), cart_items_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
