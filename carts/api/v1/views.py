from decimal import Decimal

from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from orders.models import Order, OrderItem
from orders.api.v1.serializers import OrderSerializer
from products.models import Product
from ...models import Cart, CartItem
from .serializers import CartSerializer


class CartDetail(RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


@api_view(['POST'])
def create_cart(request):
    instance = Cart.objects.create()
    serializer = CartSerializer(instance)
    return Response(serializer.data)


@api_view(['POST'])
def add_product(request, pk):
    instance = get_object_or_404(Cart, pk=pk)
    product_pk = request.data['product_pk']
    if CartItem.objects.filter(product=product_pk).first():
        raise ParseError(_('The product already exists in the cart'))

    product = Product.objects.get(pk=product_pk)
    quantity = request.data['quantity']
    if quantity % product.amount_per_package:
        raise ParseError(_('The quantity is not compatible with the amount per package'))
    if quantity > product.max_availability:
        raise ParseError(_('Quantity is greater than max availability'))
    if quantity < product.minimun:
        raise ParseError(_(f'Quantity is less than the minimun ({product.minimun})'))

    CartItem.objects.create(cart=instance, product=product, quantity=quantity)

    serializer = CartSerializer(instance)
    return Response(serializer.data)


@api_view(['PUT'])
def change_quantity(request, pk):
    instance = get_object_or_404(Cart, pk=pk)
    product_pk = request.data['product_pk']
    cart_item = CartItem.objects.filter(product=product_pk).first()
    if not cart_item:
        raise ParseError(_('The product must be added to cart first'))

    product = Product.objects.get(pk=product_pk)
    quantity = request.data['quantity']
    if quantity % product.amount_per_package:
        raise ParseError(_('The quantity is not compatible with the amount per package'))
    if quantity > product.max_availability:
        raise ParseError(_('Quantity is greater than max availability'))
    if quantity < product.minimun:
        raise ParseError(_(f'Quantity is less than the minimun ({product.minimun})'))

    cart_item.quantity = quantity
    cart_item.save()

    serializer = CartSerializer(instance)
    return Response(serializer.data)


@api_view(['DELETE'])
def remove_product(request, pk, product_pk):
    instance = get_object_or_404(Cart, pk=pk)
    cart_item = CartItem.objects.filter(cart=pk, product=product_pk).first()
    if not cart_item:
        raise ParseError(_('The product must be added to cart first'))

    cart_item.delete()
    serializer = CartSerializer(instance)
    return Response(serializer.data)


@api_view(['POST'])
def finish(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    cart_items = cart.cartitem_set.all()
    if not cart_items.first():
        raise ParseError(_('There are no products in the cart'))

    order = Order.objects.create(total_price=0.0)

    order_items = []
    for item in cart_items:
        product = item.product
        order_item = OrderItem(
            order=order,
            product=product,
            quantity=item.quantity,
            price=product.price,
            minimun=product.minimun,
            amount_per_package=product.amount_per_package,
        )
        order_items.append(order_item)
    OrderItem.objects.bulk_create(order_items)

    total_price = Decimal('0.00')
    for item in order_items:
        total_price += item.price * item.quantity
    order.total_price = total_price
    order.save()

    cart_items.delete()

    serializer = OrderSerializer(order)
    return Response(serializer.data)
