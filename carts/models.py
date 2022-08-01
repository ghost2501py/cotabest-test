from django.db import models
from django.utils.translation import gettext_lazy as _


class Cart(models.Model):
    pass


class CartItem(models.Model):
    quantity = models.IntegerField(_('Quantity'))

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
