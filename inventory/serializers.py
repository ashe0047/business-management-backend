from rest_framework import serializers
from inventory.models import *

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

class InventoryCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryCategory
        fields = '__all__'
        read_only_fields = ['cat_id']

class ServicePackageSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'] = self.service_build_field()
        
    
    def service_build_field(self, *args, **kwargs):
        if self.context.get('request', {}) and self.context['request'].method in ['PUT', 'PATCH', 'POST']:
            return serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), required=True, write_only=True, many=True, *args, **kwargs)
        else:
            return ServiceSerializer(read_only=True, many=True, *args, **kwargs)
    class Meta:
        model = ServicePackage
        fields = '__all__'
        read_only_fields = ['pkg_id']



class ServicePackageServiceSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.fields['pkg'] = ServicePackageSerializer()

    class Meta:
        model = ServicePackageService
        fields = '__all__'
        read_only_fields = ['sps_id']
