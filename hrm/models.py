from django.db import models
from auth_core.models import User
from django.core.validators import RegexValidator

class BankDatabase(models.Model):
    bank_name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    bank_swift_code = models.CharField(max_length=11, validators=[
        RegexValidator(r'^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$', message='Invalid SWIFT code')
    ], unique=True, blank=False, null=False)
    bank_city = models.CharField(max_length=100, validators=[
        RegexValidator(r'^[A-Za-z\s]+$', message='City name can only contain letters and spaces')
    ])

    class Meta:
        db_table = 'bank_database'

class Employee(models.Model):
    emp_id = models.BigAutoField(primary_key=True)
    emp_name = models.CharField(max_length=150, blank=False, null=False)
    emp_dob = models.DateField(blank=False, null=False)
    emp_address = models.CharField(max_length=1000, blank=False, null=False)
    emp_nric = models.CharField(max_length=50, blank=False, null=False)
    emp_phone_num = models.CharField(max_length=50, blank=False, null=False)
    emp_salary = models.DecimalField(max_digits=1000, decimal_places=10, null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee', null=True, blank=True)
    
    class Meta:
        db_table = 'employee'
        unique_together = (('emp_nric',), ('emp_phone_num',),)


class EmployeeBankAccount(models.Model): #Junction table for employee and bank database with extra fields to store bank acc number etc
    bank_acc_id = models.BigAutoField(primary_key=True)
    bank = models.ForeignKey(BankDatabase, on_delete=models.PROTECT)
    bank_acc_num = models.CharField(max_length=150, blank=False, null=False)
    bank_acc_type = models.CharField(max_length=100, blank=False, null=False)
    emp = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='employeebankaccount')

    class Meta:
        db_table = 'employee_bank_account'
        unique_together = (('bank_acc_num',),)

    

class EmployeeBenefitAccount(models.Model):
    benefit_acc_id = models.BigAutoField(primary_key=True)
    benefit_acc_name = models.CharField(max_length=150, blank=False, null=False)
    benefit_acc_type = models.CharField(max_length=100, blank=False, null=False)
    benefit_acc_num = models.CharField(max_length=150, blank=False, null=False)
    emp = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='employeebenefitaccount')

    class Meta:
        db_table = 'employee_benefit_account'
        unique_together = (('benefit_acc_num',),)

