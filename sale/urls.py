from django.urls import path

from sale.views import SaleViewSet
from user.views import UserViewSet

urlpatterns = [
    path('estimate/sales', SaleViewSet.as_view({
        'get': 'estimate',
    })),


]
