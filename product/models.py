from datetime import datetime

from django.db import models


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    additional_information = models.TextField()
    acquisition_date = models.BigIntegerField(default=datetime.now().timestamp() * 1000)
    acquisition_value = models.BigIntegerField()
