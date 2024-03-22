from rest_framework import serializers
from inventory.models import *
from inventory.serializers.validators import ProductValidator, ServicePackageValidator, ServiceValidator

class InventoryCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryCategory
        fields = '__all__'
        read_only_fields = ['id']

class ProductBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrand
        fields = '__all__'
        read_only_fields = ['id']

class ProductUnitSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUnitSize
        fields = '__all__'
        read_only_fields = ['id']

class ProductPackageSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPackageSize
        fields = '__all__'
        read_only_fields = ['id']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'
        read_only_fields = ['id']

class BaseProductSerializer(serializers.ModelSerializer):

    def get_validators(self):
        custom_validators = super().get_validators()
        default_validators = self.get_unique_together_validators() + self.get_unique_for_date_validators()
        return custom_validators+default_validators
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['prod_id']
        validators = [ProductValidator()]

class ProductReadSerializer(BaseProductSerializer):
    prod_category = InventoryCategorySerializer(read_only=True)
    prod_brand = serializers.CharField(read_only=True, source='prod_brand.name')
    prod_variant = serializers.CharField(read_only=True, source='prod_variant.name')
    
class ProductWriteSerializer(BaseProductSerializer):
    pass    

class ProductSupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductSupplier
        fields = '__all__'
        read_only_fields = ['id']

class ServiceSerializer(serializers.ModelSerializer):
    service_category = InventoryCategorySerializer(read_only=True)

    def get_validators(self):
        custom_validators = super().get_validators()
        default_validators = self.get_unique_together_validators() + self.get_unique_for_date_validators()
        return custom_validators+default_validators
    
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ['service_id']
        validators = [ServiceValidator()]



class ServicePackageSerializer(serializers.ModelSerializer):
    pkg_category = InventoryCategorySerializer(read_only=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'] = self.service_build_field()
        
    
    def service_build_field(self, *args, **kwargs):
        if self.context.get('request', {}) and self.context['request'].method in ['PUT', 'PATCH', 'POST']:
            return serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), required=True, write_only=True, many=True, *args, **kwargs)
        else:
            return ServiceSerializer(read_only=True, many=True, *args, **kwargs)
    
    def get_validators(self):
        custom_validators = super().get_validators()
        default_validators = self.get_unique_together_validators() + self.get_unique_for_date_validators()
        return custom_validators+default_validators
    
    class Meta:
        model = ServicePackage
        fields = '__all__'
        read_only_fields = ['pkg_id']
        validators = [ServicePackageValidator()]




class ServicePackageServiceSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.fields['pkg'] = ServicePackageSerializer()

    class Meta:
        model = ServicePackageService
        fields = '__all__'
        read_only_fields = ['sps_id']
