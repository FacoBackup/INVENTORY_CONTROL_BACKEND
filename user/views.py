import hashlib
from datetime import datetime

import jwt
from rest_framework import viewsets
from rest_framework.response import Response

from user.models import User
from user.serializer import UserSerializer
import django.core.exceptions as exceptions


class UserViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        decrypted_token = jwt.decode(
            request.META.get('HTTP_AUTHORIZATION'),
            key='askdasdiuh123i1y98yejas9d812hiu89dqw9',
            algorithms='HS256'
        ) if request.META.get('HTTP_AUTHORIZATION', None) is not None else None

        if decrypted_token is not None and decrypted_token.get('user_id', None) is not None:
            try:
                user = User.objects.get(id=pk)
                return Response(UserSerializer(user).data)
            except User.DoesNotExist:
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
                users = User.objects.all()
                return Response(UserSerializer(users, many=True))
            except exceptions.FieldError:
                return Response(status=500)

        else:
            return Response(status=401)

    def create(self, request):

        password = hashlib.sha256(request.data.get('password', None).encode())

        user = UserSerializer(data={
            'name': request.data.get('name', None),
            'email': request.data.get('email', None),
            'password': password
        })

        if user.is_valid(raise_exception=True):
            user.save()
            return Response(user.data, status=201)
        else:
            return Response(user.errors, status=400)

    def login(self, request):
        try:
            user = User.objects.get(email=request.data.get('email', None))
            password = hashlib.sha256(request.data.get('password', None).encode())

            if password == user.password:
                encoded_jwt = jwt.encode({
                    'user_id': user.id,
                    'exp': datetime.now().timestamp() * 1000 + 604800000,
                }, 'askdasdiuh123i1y98yejas9d812hiu89dqw9', algorithm='HS256')
                return Response(encoded_jwt, status=202)
            else:
                return Response(status=401)
        except User.DoesNotExist:
            return Response(status=404)
