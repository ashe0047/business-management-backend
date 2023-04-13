from rest_framework.serializers import ModelSerializer
from rest_framework.fields import empty
from hrm.models import *

class EmployeeBankAccountSerializer(ModelSerializer):

    def create(self, validated_data):
        emp_id = self.context.get('emp_id')
        validated_data['emp_id'] = emp_id
        return super().create(validated_data)
    
    class Meta:
        model = EmployeeBankAccount
        fields = ('bank_acc_id', 'bank_name', 'bank_acc_num', 'bank_acc_type', 'bank_routing_num')
        read_only_fields = ['bank_acc_id']


class EmployeeBenefitAccountSerializer(ModelSerializer):

    def create(self, validated_data):
        emp_id = self.context.get('emp_id')
        validated_data['emp_id'] = emp_id
        return super().create(validated_data)
    class Meta:
        model = EmployeeBenefitAccount
        fields = ('benefit_acc_id', 'benefit_acc_name', 'benefit_acc_type', 'benefit_acc_num')
        read_only_fields = ['benefit_acc_id']

class EmployeeSerializer(ModelSerializer):
    employeebankaccount = EmployeeBankAccountSerializer(required=False, many=True)
    employeebenefitaccount = EmployeeBenefitAccountSerializer(required=False, many=True)

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        if self.context['request'].method in ['PUT', 'PATCH']:
            self.fields['emp_salary'].read_only = True
    
    class Meta:
        model = Employee
        fields = ('emp_id', 'emp_name', 'emp_dob', 'emp_address', 'emp_nric', 'emp_phone_num', 'emp_salary', 'employeebankaccount', 'employeebenefitaccount')
        read_only_fields = ['emp_id']
 
    # def create(self, validated_data):

    #     bank_accounts_data = validated_data.pop('bank_accounts')
    #     benefit_accounts_data = validated_data.pop('benefit_accounts')

    #     employee = Employee.objects.create(**validated_data)

    #     for bank_account in bank_accounts_data:
    #         EmployeeBankAccount.objects.create(emp=employee, **bank_account)
    #     for benefit_account in benefit_accounts_data:
    #         EmployeeBenefitAccount.objects.create(emp=employee, **benefit_account)
        
    #     return employee
        
