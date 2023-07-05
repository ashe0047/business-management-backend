from rest_framework import serializers
from rest_framework.fields import empty
from pos.models.models import *
from pos.serializers.fields import *
from pos.serializers.validators import *
from crm.serializers import CustomerSerializer
from inventory.serializers import ServicePackageSerializer, ServiceSerializer, ProductSerializer

class BasePackageSubscriptionSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['pkg'] = self.pkg_build_field(context=self.context)
        # Check if the serializer is used as a nested serializer
        from pos.serializers.sale_serializers import BaseSaleItemSaleSerializer, BaseSaleItemSerializer
        if self._context.get('parent'):
            self.fields['pkg_sub_id'] = serializers.IntegerField(required=False)
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
        fields = ('pkg_sub_id', 'pkg', 'cust', 'paid_amt')
        read_only_fields = ('cust',)
        extra_kwargs = {
            "pkg_sub_id": {"required": False}
        }

class PackageSubscriptionWriteSerializer(BasePackageSubscriptionSerializer):
    cust = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=True, write_only=True)
    pkg = serializers.PrimaryKeyRelatedField(queryset=ServicePackage.objects.all(), required=True, write_only=True)
    
class PackageSubscriptionReadSerializer(BasePackageSubscriptionSerializer):
    cust = CustomerSerializer(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pkg'] = ServicePackageSerializer(read_only=True, context=self.context)


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