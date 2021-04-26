from datetime import datetime

from django.db import models

from product.models import Product
from user.models import User


class Sale(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    time_of_creation = models.BigIntegerField(default=datetime.now().timestamp() * 1000)


class SaleProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    unitary_price = models.BigIntegerField()
    quantity = models.IntegerField()
