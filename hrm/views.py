from rest_framework.generics import *
from rest_framework.viewsets import ModelViewSet
from django.db import transaction
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from hrm.models import *
from hrm.serializers import *
from hrm.permissions import *
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
# from hrm.permissions import DeleteCustomerPerm
# Create your views here.


class EmployeeView(CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = [IsAuthenticated, CreateEmployeeRecordPermission]    
    
    def create(self, request, *args, **kwargs):
        bank_accounts_data = []
        benefit_accounts_data = []
    
        if 'employeebankaccount' in request.data:
            bank_accounts_data = request.data.pop('employeebankaccount', [])

        if 'employeebenefitaccount' in request.data:
            benefit_accounts_data = request.data.pop('employeebenefitaccount', [])

        employee_serializer = self.get_serializer(data=request.data)
        employee_serializer.is_valid(raise_exception=True)
        employee = employee_serializer.save()

        for bank_account_data in bank_accounts_data:
            bank_account_serializer = EmployeeBankAccountSerializer(data=bank_account_data, context={'emp_id': employee.emp_id})
            bank_account_serializer.is_valid(raise_exception=True)
            bank_account_instance = bank_account_serializer.save()
            employee.employeebankaccount.add(bank_account_instance)


        for benefit_account_data in benefit_accounts_data:
            benefit_account_serializer = EmployeeBenefitAccountSerializer(data=benefit_account_data, context={'emp_id': employee.emp_id})
            benefit_account_serializer.is_valid(raise_exception=True)
            benefit_account_instance = benefit_account_serializer.save()
            employee.employeebenefitaccount.add(benefit_account_instance)


        headers = self.get_success_headers(employee_serializer.data)
        return Response(employee_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_object(self):
        employee = Employee.objects.filter(user=self.request.user)
        prefetch_accounts = Prefetch('employeebankaccount', queryset=EmployeeBankAccount.objects.all())
        prefetch_benefits = Prefetch('employeebenefitaccount', queryset=EmployeeBenefitAccount.objects.all())
        employee = employee.prefetch_related(prefetch_accounts, prefetch_benefits).first()
        return employee

    def update(self, request, *args, **kwargs):
        employee = self.get_object()

        if 'employeebankaccount' in request.data:
            bank_accounts_data = request.data.pop('employeebankaccount', [])
            EmployeeBankAccount.objects.filter(emp=employee).delete()
            for bank_account_data in bank_accounts_data:
                bank_account_serializer = EmployeeBankAccountSerializer(data=bank_account_data, context={'emp_id': employee.emp_id})
                bank_account_serializer.is_valid(raise_exception=True)
                bank_account_instance = bank_account_serializer.save()
                employee.employeebankaccount.add(bank_account_instance)

        if 'employeebenefitaccount' in request.data:
            benefit_accounts_data = request.data.pop('employeebenefitaccount', [])
            EmployeeBenefitAccount.objects.filter(emp=employee).delete()
            for benefit_account_data in benefit_accounts_data:
                benefit_account_serializer = EmployeeBenefitAccountSerializer(data=benefit_account_data, context={'emp_id': employee.emp_id})
                benefit_account_serializer.is_valid(raise_exception=True)
                benefit_account_instance = benefit_account_serializer.save()
                employee.employeebenefitaccount.add(benefit_account_instance)

        employee_serializer = self.get_serializer(employee, data=request.data)
        employee_serializer.is_valid(raise_exception=True)
        employee_serializer.save()

        return Response(employee_serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        employee = self.get_object()
        # Update related models if necessary
        if 'employeebankaccount' in request.data:
            bank_account_data = request.data.pop('employeebankaccount', [])
            for bank_account in bank_account_data:
                #bank account record existence is checked using bank_acc_id value from request body to allow other fields to be updated
                bank_account_instance = employee.employeebankaccount.filter(bank_acc_id=bank_account['bank_acc_id'])
                if bank_account_instance.exists():
                    bank_account_serializer = EmployeeBankAccountSerializer(
                        instance=bank_account_instance.first(),
                        data=bank_account,
                        partial=True
                    )
                    bank_account_serializer.is_valid(raise_exception=True)
                    bank_account_serializer.save()
                else:
                    bank_account_serializer = EmployeeBankAccountSerializer(data=bank_account, context={'emp_id': employee.emp_id})
                    bank_account_serializer.is_valid(raise_exception=True)
                    new_bank_account_instance = bank_account_serializer.save()
                    employee.employeebankaccount.add(new_bank_account_instance)

        if 'employeebenefitaccount' in request.data:
            benefit_account_data = request.data.pop('employeebenefitaccount', [])
            for benefit_account in benefit_account_data:
                #benefit account record existence is checked using benefit_acc_id value from request body to allow other fields to be updated
                benefit_account_instance = employee.employeebenefitaccount.filter(benefit_acc_id=benefit_account['benefit_acc_id'])
                if benefit_account_instance.exists():
                    benefit_account_serializer = EmployeeBenefitAccountSerializer(
                        instance=benefit_account_instance.first(),
                        data=benefit_account,
                        partial=True
                    )
                    benefit_account_serializer.is_valid(raise_exception=True)
                    benefit_account_serializer.save()
                else:
                    benefit_account_serializer = EmployeeBenefitAccountSerializer(data=benefit_account, context={'emp_id': employee.emp_id})
                    benefit_account_serializer.is_valid(raise_exception=True)
                    new_benefit_account_instance = benefit_account_serializer.save()
                    employee.employeebenefitaccount.add(new_benefit_account_instance)

        serializer = self.get_serializer(employee, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


        employee = self.get_object()
        serializer = self.get_serializer(employee, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Update related models if necessary
        if 'bank_account_data' in request.data:
            bank_account_data = request.data['bank_account_data']
            bank_account_serializer = EmployeeBankAccountSerializer(
                instance=employee.employeebankaccount_set,
                data=bank_account_data,
                partial=True
            )
            bank_account_serializer.is_valid(raise_exception=True)
            bank_account_serializer.save()

        if 'benefit_account_data' in request.data:
            benefit_account_data = request.data['benefit_account_data']
            benefit_account_serializer = EmployeeBenefitAccountSerializer(
                instance=employee.employeebenefitaccount_set,
                data=benefit_account_data,
                partial=True
            )
            benefit_account_serializer.is_valid(raise_exception=True)
            benefit_account_serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="delete",
                description= "Specify 'benefitaccount' or 'bankaccount' to delete only that record, or leave empty to delete the entire employee record",
                required=False,
                type=str,
                location=OpenApiParameter.QUERY),
            OpenApiParameter(
                name="id",
                description="Only required for deletion of bankaccount/benefitaccount record",
                required=False,
                type=int,
                location=OpenApiParameter.QUERY
                )
            ],
        responses={
            '404': OpenApiResponse(response=str, examples=[OpenApiExample(name="404",value={"error": "error_message"})]),
            '204': OpenApiResponse(examples=[OpenApiExample(name='204', description='No message will be returned')])
        }
    )
    def delete(self, request, *args, **kwargs):
        employee = self.get_object()
        delete_param = request.query_params.get('delete')
        if employee:
            if delete_param == 'benefitaccount':
                id_param = request.query_params.get('id')
                employee.employeebenefitaccount.filter(benefit_acc_id=id_param).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif delete_param == 'bankaccount':
                id_param = request.query_params.get('id')
                employee.employeebankaccount.filter(bank_acc_id=id_param).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                EmployeeBankAccount.objects.filter(emp=employee).delete()
                EmployeeBenefitAccount.objects.filter(emp=employee).delete()
                return super().delete(request, *args, **kwargs)
        else:
            return Response({'error': 'No employee record associated with this user account found'}, status=status.HTTP_404_NOT_FOUND)

class EmployeeListView(ListAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = [IsAuthenticated, ViewAllEmployeeRecordPermission]
    
class GetEmployeeViewWithAccounts(RetrieveAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        employee = Employee.objects.filter(user=self.request.user)
        prefetch_accounts = Prefetch('employeebankaccount', queryset=EmployeeBankAccount.objects.all(), to_attr='bank_accounts')
        prefetch_benefits = Prefetch('employeebenefitaccount', queryset=EmployeeBenefitAccount.objects.all(), to_attr='benefit_accounts')
        employee = employee.prefetch_related(prefetch_accounts, prefetch_benefits).first()
        return employee
    # def get_object(self):
    #     queryset = self.get_queryset()
    #     obj = get_object_or_404(queryset, user=self.request.user)
    #     return obj

class BankDatabaseViewset(ModelViewSet):
    serializer_class = BankDatabaseSerializer
    queryset = BankDatabase.objects.all()
    # permission_classes = [IsAdminUser, IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
 