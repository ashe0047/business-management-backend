from django.db import models
from auth_core.models import User

class Employee(models.Model):
    emp_id = models.BigAutoField(primary_key=True)
    emp_name = models.CharField(max_length=150, blank=False, null=False)
    emp_dob = models.DateField(blank=False, null=False)
    emp_address = models.CharField(max_length=1000, blank=False, null=False)
    emp_nric = models.BigIntegerField(blank=False, null=False)
    emp_phone_num = models.BigIntegerField(blank=False, null=False)
    emp_salary = models.DecimalField(max_digits=1000, decimal_places=10, null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee', null=True, blank=True)
    
    class Meta:
        db_table = 'employee'
        unique_together = (('emp_name', 'emp_nric', 'emp_phone_num'),)

class EmployeeBankAccount(models.Model):
    bank_acc_id = models.BigAutoField(primary_key=True)
    bank_name = models.CharField(max_length=150, blank=False, null=False)
    bank_acc_num = models.BigIntegerField(blank=False, null=False)
    bank_acc_type = models.CharField(max_length=100, blank=False, null=False)
    bank_routing_num = models.IntegerField(blank=True, null=True)
    emp = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='employeebankaccount')

    class Meta:
        db_table = 'employee_bank_account'
        unique_together = (('bank_acc_num', 'emp'),)

class EmployeeBenefitAccount(models.Model):
    benefit_acc_id = models.BigAutoField(primary_key=True)
    benefit_acc_name = models.CharField(max_length=150, blank=False, null=False)
    benefit_acc_type = models.CharField(max_length=100, blank=False, null=False)
    benefit_acc_num = models.BigIntegerField(blank=False, null=False)
    emp = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='employeebenefitaccount')

    class Meta:
        db_table = 'employee_benefit_account'
        unique_together = (('emp', 'benefit_acc_num'),)