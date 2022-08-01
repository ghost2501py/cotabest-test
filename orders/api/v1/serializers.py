from rest_framework import serializers

from ...models import Order, OrderItem


class OrderItemSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        item = instance.__dict__
        item['name'] = instance.product.name
        item['id'] = instance.product.id
        item['price'] = '{:.2f}'.format(item['price'])
        del item['_state']
        del item['product_id']
        del item['order_id']
        return item


class OrderSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        items = []
        for item_obj in instance.orderitem_set.all():
            item = OrderItemSerializer(item_obj).data
            items.append(item)
        return {
            'id': instance.id,
            'total_price': '{:.2f}'.format(instance.total_price),
            'items': items,
        }
