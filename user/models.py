from datetime import datetime

from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    email = models.TextField(unique=True)
    join_date = models.BigIntegerField(default=datetime.now().timestamp() * 1000)
    password = models.TextField()
