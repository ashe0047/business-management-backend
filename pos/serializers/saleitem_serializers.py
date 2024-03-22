from rest_framework import serializers
from rest_framework.serializers import DjangoValidationError, SkipField, set_value, Mapping, api_settings, get_error_detail
from pos.serializers.validators import *
from pos.serializers.fields import *
from pos.utils import update_pkg_sub_payment
from pos.serializers.pkg_sub_serializers import *
from inventory.serializers.serializers import ServiceSerializer, ProductWriteSerializer, ProductReadSerializer
from drf_spectacular.types import OpenApiTypes


class BaseSaleItemSerializer(serializers.ModelSerializer):
    '''
    :sales_item_total_price:
    :sales_item_unit_price:
        Price fields are implemented as custom fields that is read_only as:
            1. Price field is made a calculated/derived field instead of taking input directly from user thus making it not writable
            2. A read only field will not be involved in deserialization thus not involved in the calling of to_internal_value method
            3. This in turn prevents the opportunities of inserting the calculated value in to primitive data and allow validation of the data through the corresponding field
            4. This calculated data has to be done at the model level instead of serializer
    '''
    #read only fields for returning value after write HTTP methods and GET method
    sales_item_unit_price = SaleItemUnitPriceField(source='*', read_only=True)
    sales_item_total_price = SaleItemTotalPriceField(source='*', read_only=True)

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

    def get_validators(self):
        custom_validators = super().get_validators()
        default_validators = self.get_unique_together_validators() + self.get_unique_for_date_validators()
        return custom_validators+default_validators

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
    

    class Meta:
        model = SaleItem
        fields = ('sales_item_id', 'sales', 'service', 'pkg_sub', 'prod', 'sale_item_type', 'sales_item_qty', 'sales_item_unit_price', 'sales_item_total_price')
        read_only_fields = ('sales_item_id', )
        validators = [VoucherUseValidator(), SaleItemValidator()]

class SaleItemWriteSerializer(BaseSaleItemSerializer):
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), required=False)
    prod = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pkg_sub'] = self.pkg_sub_build_field(required=False, context=self.context_update_parent())
        self.fields['voucher_sale'] = self.voucher_sale_build_field(required=False)
        self.fields['voucher_use'] = self.voucher_use_build_field(required=False)
        

    def pkg_sub_build_field(self, *args, **kwargs):
        return PackageSubscriptionWriteSerializer(*args, **kwargs)
    
    def voucher_use_build_field(self, *args, **kwargs):
        return VoucherUseField(*args, **kwargs)
    
    def voucher_sale_build_field(self, *args, **kwargs):
        return VoucherSaleField(*args, **kwargs)
    
    #Custom saleitem creation for handling creation of nested pkg_sub
    def create(self, validated_data):
        if 'pkg_sub' in validated_data:
            pkg_sub = validated_data.pop('pkg_sub', {})
            #payment handler for existing pkg_sub
            if 'pkg_sub_id' in pkg_sub:
                pkg_sub_id = pkg_sub.pop('pkg_sub_id', None)
                pkg_sub_instance = update_pkg_sub_payment(pkg_sub_id, self, pkg_sub['paid_amt'])
            else:
                #retrieve customer_id
                pkg_sub['cust'] = validated_data['sales'].cust
                pkg_sub_instance = self.fields['pkg_sub'].Meta.model.objects.create(**pkg_sub)
            validated_data['pkg_sub'] = pkg_sub_instance

        saleitem_instance = self.Meta.model.objects.create(**validated_data)

        return saleitem_instance  

    def update(self, instance, validated_data):
        special_fields = ['prod', 'service', 'pkg_sub']
        #reset existing special fields in saleitem
        for field in special_fields:
            if field in validated_data:
                for existing_field in special_fields:
                    #unlink and delete only if exisiting field for saleitem is pkg_sub
                    setattr(instance, existing_field, None)
        
        old_pkg_sub = None
        if 'pkg_sub' in validated_data:
            pkg_sub = validated_data.pop('pkg_sub',{})
            old_pkg_sub = instance.pkg_sub
            #customer auto obtained from the sales instance retrieved from request data as this field is mandatory in PUT method
            pkg_sub['cust'] = validated_data['sales'].cust
            pkg_sub_instance = self.fields['pkg_sub'].Meta.model.objects.create(**pkg_sub)
            validated_data['pkg_sub'] = pkg_sub_instance
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        #saleitem is linked to new pkg_sub if it exists after saving
        instance.save()
        # if there is existing pkg_sub linked that is obsolete, it will be deleted
        if old_pkg_sub is not None:
            #pkg_sub delete method will automatically delete the related entry in junction table so that protected error will not be raised
            old_pkg_sub.delete()
        
        return instance
    
    # # for response data representation
    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     sales_item_unit_price = {
    #         'gross': ret.pop('gross_sales_item_unit_price', None),
    #         'net': ret.pop('net_sales_item_unit_price', None)
    #     }
    #     sales_item_total_price = {
    #         'gross': ret.pop('gross_sales_item_total_price', None),
    #         'net': ret.pop('net_sales_item_total_price', None)
    #     }
    #     ret.update({
    #         'sales_item_unit_price': sales_item_unit_price,
    #         'sales_item_total_price': sales_item_total_price
    #     })
    #     return ret
    
class SaleItemReadSerializer(BaseSaleItemSerializer):
    service = ServiceSerializer(read_only=True)
    prod = ProductReadSerializer(read_only=True)
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pkg_sub'] = self.pkg_sub_build_field(context=self.context_update_parent())
        self.fields['voucher_sale'] = self.voucher_sale_build_field()
        self.fields['voucher_use'] = self.voucher_use_build_field()


    # @extend_schema_field(
    # field = {'type': 'object',
    #             'properties': {
    #                 'gross_sale_item_total_price': {
    #                     'type': 'number',
    #                     'format': 'double'
    #                 },
    #                 'net_sale_item_total_price': {
    #                     'type': 'number',
    #                     'format': 'double'
    #                 },
    #             },}
    # )   
    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     sales_item_unit_price = {
    #         'gross': ret.pop('gross_sales_item_unit_price', None),
    #         'net': ret.pop('net_sales_item_unit_price', None)
    #     }
    #     sales_item_total_price = {
    #         'gross': ret.pop('gross_sales_item_total_price', None),
    #         'net': ret.pop('net_sales_item_total_price', None)
    #     }
    #     ret.update({
    #         'sales_item_unit_price': sales_item_unit_price,
    #         'sales_item_total_price': sales_item_total_price
    #     })
    #     return ret
    
    def pkg_sub_build_field(self, *args, **kwargs):
        return PackageSubscriptionReadSerializer(*args, **kwargs)
    
    def voucher_use_build_field(self, *args, **kwargs):
        return VoucherUseField(*args, **kwargs)
    
    def voucher_sale_build_field(self, *args, **kwargs):
        return VoucherSaleField(*args, **kwargs)
    