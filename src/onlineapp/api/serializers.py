
from rest_framework import serializers
from onlineapp.models import Category, Product, Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model= Order
        fields = '__all__'

    def create(self, validate_data):
        return Order.objects.create(**validate_data)