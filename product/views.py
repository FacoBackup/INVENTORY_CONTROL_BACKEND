import jwt
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from product.models import Product
from product.serializer import ProductSerializer
import django.core.exceptions as exceptions


class ProductViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        decrypted_token = jwt.decode(
            request.META.get('HTTP_AUTHORIZATION'),
            key='askdasdiuh123i1y98yejas9d812hiu89dqw9',
            algorithms='HS256'
        ) if request.META.get('HTTP_AUTHORIZATION', None) is not None else None

        if decrypted_token is not None and decrypted_token.get('user_id', None) is not None:
            try:
                product = Product.objects.get(id=pk)
                return Response(ProductSerializer(product).data)
            except Product.DoesNotExist:
                return Response(status=404)
        else:
            return Response(status=401)

    def list(self, request):
        decrypted_token = jwt.decode(
            request.META.get('HTTP_AUTHORIZATION'),
            key='askdasdiuh123i1y98yejas9d812hiu89dqw9',
            algorithms='HS256'
        ) if request.META.get('HTTP_AUTHORIZATION', None) is not None else None

        if decrypted_token is not None and decrypted_token.get('user_id', None) is not None:
            try:
                products = Product.objects.all()
                return Response(ProductSerializer(products, many=True))
            except exceptions.FieldError:
                return Response(status=500)

        else:
            return Response(status=401)

    def create(self, request):
        decrypted_token = jwt.decode(
            request.META.get('HTTP_AUTHORIZATION'),
            key='askdasdiuh123i1y98yejas9d812hiu89dqw9',
            algorithms='HS256'
        ) if request.META.get('HTTP_AUTHORIZATION', None) is not None else None

        if decrypted_token is not None and decrypted_token.get('user_id', None) is not None:

            product = ProductSerializer(data=request.data)

            if product.is_valid(raise_exception=True):
                product.save()
                return Response(product.data, status=201)
            else:
                return Response(product.errors, status=400)
        else:
            return Response(status=401)
