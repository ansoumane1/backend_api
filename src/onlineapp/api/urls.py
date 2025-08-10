from django.urls import path
from .views import OrderAPIView


urlpatterns = [
    path('orders/', OrderAPIView.as_view(), name='order-list'),
]