from django.db import models
from django.utils.translation import ugettext_lazy as _


class Product(models.Model):
    name = models.CharField(_('Name'), max_length=150, unique=True)
    price = models.DecimalField(_('Price'), max_digits=6, decimal_places=2)
    minimun = models.IntegerField(_('Minimun'))
    amount_per_package = models.IntegerField(_('Amount per package'))
    max_availability = models.IntegerField(_('Max availability'))
