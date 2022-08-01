from decimal import Decimal

from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from django.utils.translation import gettext_lazy as _

from orders.models import Order, OrderItem
from orders.api.v1.serializers import OrderSerializer
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
    instance = Cart.objects.get(pk=pk)
    product = request.data['product_pk']
    if CartItem.objects.filter(product=product).first():
        raise APIException(_('The product already exists in the cart'))

    quantity = request.data['quantity']
    CartItem.objects.create(cart=instance, product_id=product, quantity=quantity)

    serializer = CartSerializer(instance)
    return Response(serializer.data)


@api_view(['PUT'])
def change_quantity(request, pk):
    instance = Cart.objects.get(pk=pk)
    product = request.data['product_pk']
    cart_item = CartItem.objects.filter(product=product).first()
    if not cart_item:
        raise APIException(_('The product must be added to cart first'))

    cart_item.quantity = request.data['quantity']
    cart_item.save()

    serializer = CartSerializer(instance)
    return Response(serializer.data)


@api_view(['DELETE'])
def remove_product(request, pk, product_pk):
    instance = Cart.objects.get(pk=pk)
    cart_item = CartItem.objects.filter(cart=pk, product=product_pk).first()
    if not cart_item:
        raise APIException(_('The product must be added to cart first'))

    cart_item.delete()
    serializer = CartSerializer(instance)
    return Response(serializer.data)


@api_view(['POST'])
def finish(request, pk):
    cart = Cart.objects.get(pk=pk)
    cart_items = cart.cartitem_set.all()
    if not cart_items.first():
        raise APIException(_('There are no products in the cart'))

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
