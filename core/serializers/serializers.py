from rest_framework import serializers
from core.models import *
from pos.serializers.sale_serializers import *
from pos.serializers.saleitem_serializers import *
from hrm.serializers import *
from core.utils import context_update_parent

# class CommissionSerializer(serializers.ModelSerializer):
#     sales_item = serializers.SerializerMethodField()
#     emp = serializers.SerializerMethodField()

#     def __init__(self, instance=None, data=..., **kwargs):
#         super().__init__(instance, data, **kwargs)
#         self.fields['saleitem'] = self.sales_item_build_field()
#         self.fields['emp'] = self.emp_build_field()

#     def sales_item_build_field(self, obj):
#         return BaseSaleItemSerializer()
    
#     def emp_build_field(self, obj):
#         return EmployeeSerializer(obj.data).data
    
#     class Meta:
#         model = FixedCommissionSharing
#         fields = ('com_id', 'sales_item', 'emp', 'com_amt', 'com_datetime', 'com_type')


# class CommissionSharingPlanSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CommissionSharingPlan
#         fields = ('com_sharing_id', 'com_sharing_name', 'com_sharing_desc')


class BaseEmployeeCommissionSerializer(serializers.ModelSerializer):
    emp = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['com'] = self.sales_sharing_detail_build_field(*args, **kwargs)
        # self.fields['emp'] = self.emp_build_field(*args, **kwargs)
        if self.context.get('parent'):
            self.fields.pop('com')

    def sales_sharing_detail_build_field(self, *args, **kwargs):
        return BaseCommissionSerializer(*args, **kwargs)
    
    class Meta:
        model = EmployeeCommission
        fields = ('com', 'emp', 'sales_amount')
        extra_kwargs = {
            "sales_amount": {"required": False}
        }


# class EmployeeCommissionSharingPercentageWriteSerializer(BaseEmployeeCommissionSharingPercentageSerializer):
#     emp = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=True)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

# class EmployeeCommissionSharingPercentageReadSerializer(BaseEmployeeCommissionSharingPercentageSerializer):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['emp'] = self.emp_build_field(*args, **kwargs)

#     def emp_build_field(self, *args, **kwargs):
#         return EmployeeSerializer(*args, **kwargs)

class BaseCommissionSerializer(serializers.ModelSerializer):

    def context_update_parent(self):
        #pass parent serializer to package_subscription for checking
        context = self.context.copy()
        if not context.get('parent'):
            context['parent'] = self
        else:
            context['parent2'] = self
        return context
    class Meta:
        model = Commission
        fields = ('com_id', 'sales', 'sales_item', 'custom_sharing', 'emp_share_percent')
        extra_kwargs = {
            "custom_sharing": {"required": True}
        }

class CommissionWriteSerializer(BaseCommissionSerializer):    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['emp_share_percent'] = BaseEmployeeCommissionSerializer(required=True, write_only=True, many=True, context=self.context_update_parent())
    
    def validate(self, data):
        '''
        TODO:
            1. Port validation over to validator file then test the validator
        '''
        #If custom_sharing is True
        if 'custom_sharing' in data and data['custom_sharing']:
            total_share_amount = 0
            for emp_share_percent in data['emp_share_percent']:
                #Ensure that sales_amount must exists 
                if 'sales_amount' not in emp_share_percent:
                    raise ValidationError("Custom sharing is True but sales_amount does not exists")
                #sum the total share amount if it exists
                total_share_amount += emp_share_percent['sales_amount']

            #Ensure that total sales_amount for each employee totals to the amount of sales/sales_item
            # total_share_amount = sum(emp_share_percent['sales_amount'] for emp_share_percent in data['emp_share_percent'])
            if total_share_amount != data['sales'].net_sales_amt or total_share_amount != data['sales_item'].net_sales_item_price:
                raise ValidationError("Total share amount for each employee is not equal to total sales/salesitem amount")

        #Ensure if sale item is used, the Sale that contain the sale item should not exists in Commission entry and vice versa
        if 'sales_item' in data and Commission.objects.filter(sales=data['sales_item'].sales).exists():
            raise ValidationError('Sale for this saleitem already exists in Commission and can no longer be used')
        elif 'sales' in data:
            sales_item = data['sales'].saleitem.all()
            if any(Commission.objects.filter(sales_item=item).exists() for item in sales_item):
                raise ValidationError("saleitem for this sale already exists in Commission and can no longer be used") 
            
        return data
    
class CommissionReadSerializer(BaseCommissionSerializer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['emp_share_percent'] = BaseEmployeeCommissionSerializer(many=True, read_only=True, context=self.context_update_parent(), source='employeecommission')

# class BaseEmployeeFixedCommissionSharing(serializers.ModelSerializer):

#     class Meta:
#         model = EmployeeFixedCommissionSharing
#         fields = ('com', 'emp', 'share_percent', 'sales_amount')
#         extra_kwargs = {
#             'sales_amount': {'required': False}
#         }
# class BaseFixedCommissionSharingSerializer(serializers.ModelSerializer):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['com'] = self.com_build_field(*args, **kwargs)
#         # self.fields['emp'] = self.emp_build_field(*args, **kwargs)
#         if self.context.get('parent'):
#             self.fields.pop('com')
    
#     def com_build_field(self, *args, **kwargs):
#         return BaseFixedCommissionSharingSerializer(*args, **kwargs)
#     class Meta:
#         model = FixedCommissionSharing
#         fields = ('com_id', 'sales_item', 'com_amt', 'service_com', 'voucher_com', 'emp_share_percent')

# class FixedCommissionSharingWriteSerializer(BaseFixedCommissionSharingSerializer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['emp_share_percent'] = BaseEmployeeFixedCommissionSharing(required=True, write_only=True, many=True, context=context_update_parent(self))

# class FixedCommissionSharingReadSerializer(BaseFixedCommissionSharingSerializer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['emp_share_percent'] = BaseEmployeeFixedCommissionSharing(many=True, read_only=True, context=context_update_parent(self), source='employeefixedcommissionsharing')


class ProductCommissionStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCommissionStructure
        fields = ('prod_com_id', 'prod_com_type', 'prod_com_rate')


class ServiceCommissionStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCommissionStructure
        fields = ('service_com_id', 'service_com_type', 'service_com_category', 'service_com_rate')


class VoucherCommissionStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherCommissionStructure
        fields = ('voucher_com_id', 'voucher_com_type', 'voucher_com_rate', 'voucher_com_amt')

class PercentageMultiplierThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = PercentageMultiplierThreshold
        fields = ('thres_id', 'sales_amt', 'percent_multiplier', 'bonus_amt')


