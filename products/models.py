from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(_('Name'), max_length=150, unique=True)
    price = models.DecimalField(_('Price'), max_digits=7, decimal_places=2)
    minimun = models.IntegerField(_('Minimun'))
    amount_per_package = models.IntegerField(_('Amount per package'))
    max_availability = models.IntegerField(_('Max availability'))

    def __str__(self):
        return self.name
