from django.urls import path

from user.views import UserViewSet

urlpatterns = [
    path('authenticate', UserViewSet.as_view({
        'post': 'login',
    })),
    path('user', UserViewSet.as_view({
        'post': 'create',
    })),
    path('user', UserViewSet.as_view({
        'put': 'update',
        'delete': 'delete',
        'get': 'retrieve'
    })),

]
