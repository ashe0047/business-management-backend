from rest_framework import serializers
from rest_framework.fields import empty
from core.models import *
from pos.serializers import *
from hrm.serializers import *


class BankDatabaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankDatabase
        fields = '__all__'
        read_only_fields = ['id']

class CommissionSerializer(serializers.ModelSerializer):
    sales_item = serializers.SerializerMethodField()
    emp = serializers.SerializerMethodField()

    def get_sales_item(self, obj):
        return SaleItemSerializer(obj.data).data
    
    def get_emp(self, obj):
        return EmployeeSerializer(obj.data).data
    class Meta:
        model = Commission
        fields = ('com_id', 'sales_item', 'emp', 'com_amt', 'com_datetime', 'com_type')


# class CommissionSharingPlanSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CommissionSharingPlan
#         fields = ('com_sharing_id', 'com_sharing_name', 'com_sharing_desc')

class EmployeeCommissionSharingPercentageSerializer(serializers.ModelSerializer):
    com_sharing_detail = serializers.SerializerMethodField()
    emp = serializers.SerializerMethodField()

    def get_emp(self, obj):
        return EmployeeSerializer(obj.data).data

    def get_com_sharing_detail(self, obj):
        return CommissionSharingDetailSerializer(obj.data).data
    
    class Meta:
        model = EmployeeCommissionSharingPercentage
        fields = ('com_sharing_detail', 'emp', 'share_percent')

class CommissionSharingDetailSerializer(serializers.ModelSerializer):
    sales = SaleSerializer()
    sales_item = serializers.SerializerMethodField()
    # com_sharing = CommissionSharingPlanSerializer()
    emp_share_percent = EmployeeCommissionSharingPercentageSerializer(many=True)
    
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.fields['sales_item'] = self.get_sales_item()
        
    def get_sales_item(self, *args, **kwargs):
        return SaleItemSerializer(*args, **kwargs)
    
    class Meta:
        model = CommissionSharingDetail
        fields = ('com_sharing_detail_id', 'sales', 'sales_item', 'emp_share_percent')
        
class ProductCommissionStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCommissionStructure
        fields = ('prod_com_id', 'prod_com_type', 'prod_com_rate')


class ServiceCommissionStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCommissionStructure
        fields = ('service_com_id', 'service_com_type', 'service_com_category', 'service_com_rate')


class PercentageMultiplierThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = PercentageMultiplierThreshold
        fields = ('thres_id', 'sales_amt', 'percent_multiplier')