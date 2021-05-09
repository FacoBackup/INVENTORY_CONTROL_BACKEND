from datetime import datetime

import jwt
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
import django.core.exceptions as exceptions

from sale.models import Sale, SaleProduct
from sale.serializer import SaleSerializer, SaleProductSerializer


class SaleViewSet(viewsets.ViewSet):
    def estimate(self, request):
        decrypted_token = jwt.decode(
            request.META.get('HTTP_AUTHORIZATION'),
            key='askdasdiuh123i1y98yejas9d812hiu89dqw9',
            algorithms='HS256'
        ) if request.META.get('HTTP_AUTHORIZATION', None) is not None else None

        if decrypted_token is not None and decrypted_token.get('user_id', None) is not None:
            current_date = datetime.now().timestamp() * 1000
            first_day = Sale.objects.filter(time_of_creation__lt=current_date,
                                            time_of_creation__gt=(current_date - 86400000)).count()
            second_day = Sale.objects.filter(time_of_creation__lt=(current_date - 86400000),
                                             time_of_creation__gt=(current_date - 86400000 * 2)).count()
            third_day = Sale.objects.filter(time_of_creation__lt=(current_date - 86400000 * 2),
                                            time_of_creation__gt=(current_date - 86400000 * 4)).count()
            return Response({
                'first_day': first_day,
                'second_day': second_day,
                'third_day': third_day
            })
        else:
            return Response(status=401)

    def retrieve(self, request, pk=None):
        decrypted_token = jwt.decode(
            request.META.get('HTTP_AUTHORIZATION'),
            key='askdasdiuh123i1y98yejas9d812hiu89dqw9',
            algorithms='HS256'
        ) if request.META.get('HTTP_AUTHORIZATION', None) is not None else None

        if decrypted_token is not None and decrypted_token.get('user_id', None) is not None:
            try:
                sale = Sale.objects.get(id=pk, user=decrypted_token.get('user_id'))
                return Response(SaleSerializer(sale).data)
            except Sale.DoesNotExist:
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
                sales = Sale.objects.all()
                return Response(SaleSerializer(sales, many=True))
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

            sale = SaleSerializer(data=request.data)

            if sale.is_valid(raise_exception=True):
                sale.save()
                return Response(sale.data, status=201)
            else:
                return Response(sale.errors, status=400)
        else:
            return Response(status=401)


class SaleProductViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        decrypted_token = jwt.decode(
            request.META.get('HTTP_AUTHORIZATION'),
            key='askdasdiuh123i1y98yejas9d812hiu89dqw9',
            algorithms='HS256'
        ) if request.META.get('HTTP_AUTHORIZATION', None) is not None else None

        if decrypted_token is not None and decrypted_token.get('user_id', None) is not None:
            try:
                product = SaleProduct.objects.get(id=pk)
                return Response(SaleProductSerializer(product).data)
            except SaleProduct.DoesNotExist:
                return Response(status=404)
        else:
            return Response(status=401)

    def list(self, request, fk=None):
        decrypted_token = jwt.decode(
            request.META.get('HTTP_AUTHORIZATION'),
            key='askdasdiuh123i1y98yejas9d812hiu89dqw9',
            algorithms='HS256'
        ) if request.META.get('HTTP_AUTHORIZATION', None) is not None else None

        if decrypted_token is not None and decrypted_token.get('user_id', None) is not None:
            products = SaleProduct.objects.filter(sale=fk)
            return Response(SaleProductSerializer(products, many=True).data)
        else:
            return Response(status=401)

    def create(self, request):
        decrypted_token = jwt.decode(
            request.META.get('HTTP_AUTHORIZATION'),
            key='askdasdiuh123i1y98yejas9d812hiu89dqw9',
            algorithms='HS256'
        ) if request.META.get('HTTP_AUTHORIZATION', None) is not None else None

        if decrypted_token is not None and decrypted_token.get('user_id', None) is not None:

            product = SaleProductSerializer(data=request.data)

            if product.is_valid(raise_exception=True):
                product.save()
                return Response(product.data, status=201)
            else:
                return Response(product.errors, status=400)
        else:
            return Response(status=401)
