from rest_framework import serializers
from inventory.models import Product, ProductSupplier, Service

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['prod_id']

class ProductSupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductSupplier
        fields = '__all__'
        read_only_fields = ['supplier_id']

class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ['service_id']