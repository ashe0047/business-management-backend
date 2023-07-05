from rest_framework import serializers
from crm.serializers import CustomerSerializer
from pos.serializers.validators import VoucherUseValidator
from pos.models.models import Sale
from pos.serializers.fields import SalesAmountField
from pos.serializers.saleitem_serializers import BaseSaleItemSerializer, SaleItemReadSerializer, SaleItemWriteSerializer
from marketing.models.models import GenericVoucher

class SaleSerializer(serializers.ModelSerializer):
    cust = CustomerSerializer(required=False)
    sales_amt = SalesAmountField(source='*', read_only=True)
    gen_voucher_used = serializers.PrimaryKeyRelatedField(queryset=GenericVoucher.objects.all(), required=False, many=True) #explicitly define as manytomany field is read_only by default

    def get_validators(self):
        custom_validators = super().get_validators()
        default_validators = self.get_unique_together_validators() + self.get_unique_for_date_validators()
        return custom_validators+default_validators

    class Meta:
        model = Sale
        fields = ('sales_id', 'cust', 'sales_datetime', 'sales_amt', 'sales_payment_method', 'gen_voucher_used')
        read_only_fields = ('sales_id',)
        validators = [VoucherUseValidator()]

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


    def get_validators(self):
        custom_validators = super().get_validators()
        default_validators = self.get_unique_together_validators() + self.get_unique_for_date_validators()
        return custom_validators+default_validators

    # def saleitem_build_field(self, *args, **kwargs):
    #     return SaleItemSerializer(required=True, many=True, *args, **kwargs)
    class Meta:
        model = Sale
        fields = ('sales_id', 'cust', 'sales_datetime', 'sales_amt', 'sales_payment_method', 'saleitem', 'gen_voucher_used')
        read_only_fields = ('sales_id',)
        validators = [VoucherUseValidator()]

class SaleItemSaleWriteSerializer(BaseSaleItemSaleSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['saleitem'] = SaleItemWriteSerializer(required=True, many=True, context=self.context_update_parent())
    
    # def validate(self, data):
    #     data = super().validate(data)
    #     total_sales_item_amt = sum(item['sales_item_price'] for item in data['saleitem'])
    #     if data['gross_sales_amt'] != total_sales_item_amt:
    #         raise ValidationError("Total sales amount is not equivalent to total amount of all sales item")

    #     return data
    
    def create(self, validated_data):
        #Remove the fields with nested data
        cust = validated_data.pop('cust', {})
        sales_item = validated_data.pop('saleitem', {})

        cust_nric = cust.pop('cust_nric', None)
        #if customer already exists in model, then return customer instance, else create an instance
        cust_instance, created = self.fields['cust'].Meta.model.objects.get_or_create(cust_nric=cust_nric, defaults=cust)
        validated_data['cust'] = cust_instance

        
        sales_instance = self.Meta.model.objects.create(**validated_data)
        sales_item_with_sales = [item.update({'sales': sales_instance}) for item in sales_item]
        sales_item_instances = self.fields['saleitem'].create(sales_item)
        
        #re-save sales instance to trigger sales_amt calculation after saleitems have been added
        sales_instance.save()
        
        return sales_instance
    
    def update(self, instance, validated_data):
        if 'cust' in validated_data:
            #Remove the fields with nested data
            cust = validated_data.pop('cust', {})
            cust_nric = cust.pop('cust_nric', None)
            #if customer already exists in model, then return customer instance, else create an instance
            cust_instance, created = self.fields['cust'].Meta.model.objects.get_or_create(cust_nric=cust_nric, defaults=cust)
            validated_data['cust'] = cust_instance

        if 'saleitem' in validated_data:
            sales_item = validated_data.pop('saleitem', {})
            #delete all associated saleitem instances
            instance.saleitem.all().delete()
            #create new saleitem instances using the data and assign them with the current sale instance
            sales_item_with_sales = [item.update({'sales': instance}) for item in sales_item]
            sales_item_instances = self.fields['saleitem'].create(sales_item)
        
        #update all other sale instances attributes
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance

        
class SaleItemSaleReadSerializer(BaseSaleItemSaleSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['saleitem'] = SaleItemReadSerializer(many=True, context=self.context_update_parent())
