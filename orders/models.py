import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    total_price = models.DecimalField(_('Price'), max_digits=9, decimal_places=2)


class OrderItem(models.Model):
    quantity = models.IntegerField(_('Quantity'))
    price = models.DecimalField(_('Price'), max_digits=7, decimal_places=2)
    minimun = models.IntegerField(_('Minimun'))
    amount_per_package = models.IntegerField(_('Amount per package'))

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', null=True, on_delete=models.SET_NULL)
