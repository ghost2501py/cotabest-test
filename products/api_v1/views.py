from rest_framework import generics
from django_filters import rest_framework as filters

from django.contrib.auth.models import User

from .filters import ProductFilter
from ..models import Product
from .serializers import ProductSerializer


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter
