from rest_framework import serializers

from product.models import Product
from user.models import User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
