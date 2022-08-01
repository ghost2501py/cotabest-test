from rest_framework import serializers

from ...models import Cart, CartItem


class CartItemSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        product = instance.product.__dict__
        product['price'] = '{:.2f}'.format(product['price'])
        product['quantity'] = instance.quantity
        del product['_state']
        return product


class CartSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        items = []
        for item_obj in instance.cartitem_set.all():
            item = CartItemSerializer(item_obj).data
            items.append(item)
        return {
            'id': instance.id,
            'total_price': '{:.2f}'.format(instance.total_price),
            'items': items,
        }
