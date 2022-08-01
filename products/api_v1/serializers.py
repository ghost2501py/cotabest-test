from rest_framework import serializers

from ..models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'minimun', 'amount_per_package',
            'max_availability',
        ]
