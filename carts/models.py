from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _


class Cart(models.Model):
    @property
    def total_price(self):
        price = Decimal('0.00')
        for item in self.cartitem_set.all():
            price += item.product.price * item.quantity
        return price


class CartItem(models.Model):
    quantity = models.IntegerField(_('Quantity'))

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)


