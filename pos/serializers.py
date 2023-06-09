from rest_framework import serializers
from rest_framework.fields import empty
from pos.models import *
from crm.serializers import CustomerSerializer
from inventory.serializers import ServicePackageSerializer, ServiceSerializer, ProductSerializer

class BasePackageSubscriptionSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['pkg'] = self.pkg_build_field(context=self.context)
        # Check if the serializer is used as a nested serializer
        if isinstance(self._context.get('parent'), BaseSaleItemSaleSerializer):
            # Remove cust field as the value can be obtained automatically from parent serializer
            self.fields.pop('cust', None)
        elif isinstance(self._context.get('parent'), BaseSaleItemSerializer):
            if self.context.get('request', {}) and self.context['request'].method not in ['GET']:
                #Remove field only if creating packagesubscription from saleitem as cust field value can be automatically obtained from sales_id
                self.fields.pop('cust', None)
        # else:
        #     self.fields['cust'] = self.cust_build_field()
    
    # def cust_build_field(self, *args, **kwargs):
    #     if self.context['request'].method in ['PUT', 'PATCH', 'POST']:
    #         kwargs.pop('context')
    #         return serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=True, write_only=True, *args, **kwargs)
    #     else:
    #         return CustomerSerializer(read_only=True, *args, **kwargs)
    
    # def pkg_build_field(self, *args, **kwargs):
    #     if self.context['request'].method in ['PUT', 'PATCH', 'POST']:
    #         kwargs.pop('context')
    #         return serializers.PrimaryKeyRelatedField(queryset=ServicePackage.objects.all(), required=True, write_only=True, *args, **kwargs)
    #     else:
    #         return ServicePackageSerializer(read_only=True, *args, **kwargs)
        
    class Meta:
        model = PackageSubscription
        fields = ('pkg_sub_id', 'pkg', 'cust', 'deposit_amt')
        read_only_fields = ('pkg_sub_id', 'cust')

class PackageSubscriptionWriteSerializer(BasePackageSubscriptionSerializer):
    cust = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=True, write_only=True)
    pkg = serializers.PrimaryKeyRelatedField(queryset=ServicePackage.objects.all(), required=True, write_only=True)
    
class PackageSubscriptionReadSerializer(BasePackageSubscriptionSerializer):
    cust = CustomerSerializer(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pkg'] = ServicePackageSerializer(read_only=True, context=self.context)
class SaleSerializer(serializers.ModelSerializer):
    cust = CustomerSerializer(required=False)


    class Meta:
        model = Sale
        fields = ('sales_id', 'cust', 'sales_datetime', 'sales_total_amt', 'sales_payment_type')
        read_only_fields = ('sales_id',)

class BaseSaleItemSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if the serializer is used as a nested serializer
        if self.context.get('parent'):
            # Remove the sales_id field if used as a nested serializer
            self.fields.pop('sales', None)
        

        
        # self.fields['service'] = self.service_build_field(context=context)
        # self.fields['prod'] = self.prod_build_field(context=context)
    
    def context_update_parent(self):
        #pass parent serializer to package_subscription for checking
        context = self.context.copy()
        if not context.get('parent'):
            context['parent'] = self
        else:
            context['parent2'] = self
        
        return context
        
    # def service_build_field(self, *args, **kwargs):
    #     if self.context['request'].method in ['PUT', 'PATCH', 'POST']:
    #         kwargs.pop('context')
    #         return serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), required=False, *args, **kwargs)
    #     else:
    #         return ServiceSerializer(read_only=True, *args, **kwargs)

    # def prod_build_field(self, *args, **kwargs):
    #     if self.context['request'].method in ['PUT', 'PATCH', 'POST']:
    #         kwargs.pop('context')
    #         return serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False, *args, **kwargs)
    #     else:
    #         return ProductSerializer(read_only=True, *args, **kwargs)
        
    
    def validate(self, data):      
        data = super().validate(data)

        count = 0
        for field in ['service', 'pkg_sub', 'prod']:
            if field in data and data[field] is not None:
                count += 1

        # Ensure that exactly one field has a value
        if count != 1:
            raise serializers.ValidationError("Exactly one field is required.")

        # Ensure that at least one field has a value
        if all(field not in data or data[field] is None for field in ['service', 'pkg_sub', 'prod']):
            raise serializers.ValidationError("At least one field is required.")

        return data

    class Meta:
        model = SaleItem
        fields = ('sales_item_id', 'sales', 'service', 'pkg_sub', 'prod', 'sale_item_type', 'sales_item_qty', 'sales_item_price')
        read_only_fields = ('sales_item_id',)

class SaleItemWriteSerializer(BaseSaleItemSerializer):
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), required=False)
    prod = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pkg_sub'] = self.pkg_sub_build_field(required=False, context=self.context_update_parent())
    def pkg_sub_build_field(self, *args, **kwargs):
        return PackageSubscriptionWriteSerializer(*args, **kwargs)
    
class SaleItemReadSerializer(BaseSaleItemSerializer):
    service = ServiceSerializer(read_only=True)
    prod = ProductSerializer(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pkg_sub'] = self.pkg_sub_build_field(required=False, context=self.context_update_parent())

    def pkg_sub_build_field(self, *args, **kwargs):
        return PackageSubscriptionReadSerializer(*args, **kwargs)
    
class BaseSaleItemSaleSerializer(SaleSerializer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #     self.fields['saleitem'] = self.saleitem_build_field(context=context)

    def context_update_parent(self):
        context = self.context.copy()
        if not context.get('parent'):
            context['parent'] = self
        else:
            context['parent2'] = self
        return context
    # def saleitem_build_field(self, *args, **kwargs):
    #     return SaleItemSerializer(required=True, many=True, *args, **kwargs)
    class Meta:
        model = Sale
        fields = ('sales_id', 'cust', 'sales_datetime', 'sales_total_amt', 'sales_payment_type', 'saleitem')
        read_only_fields = ('sales_id',)

class SaleItemSaleWriteSerializer(BaseSaleItemSaleSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['saleitem'] = SaleItemWriteSerializer(required=True, many=True, context=self.context_update_parent())
class SaleItemSaleReadSerializer(BaseSaleItemSaleSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['saleitem'] = SaleItemReadSerializer(many=True, context=self.context_update_parent())


# class SaleItemPackageSubscriptionSerializer(serializers.ModelSerializer):
#     pkg = serializers.PrimaryKeyRelatedField(queryset=ServicePackage.objects.all(), write_only=True, required=True)
    
#     class Meta:
#         model = PackageSubscription
#         fields = ('pkg_sub_id', 'pkg', 'deposit_amt')
#         read_only_fields = ('pkg_sub_id',)

class PackageSubscriptionServiceSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.fields['pkg_sub'] = self.pkg_sub_build_field()

    def pkg_sub_build_field(self, *args, **kwargs):
        return BasePackageSubscriptionSerializer(*args, **kwargs)
    class Meta:
        model = PackageSubscriptionService
        fields = ('pkg_sub_service_id', 'pkg_sub', 'service', 'treatment_left')
        read_only_fields = ('pkg_sub_service_id',)