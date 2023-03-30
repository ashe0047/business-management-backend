from django.db import models


class Employee(models.Model):
    emp_id = models.BigAutoField(primary_key=True)
    emp_name = models.CharField(max_length=150, blank=True, null=True)
    emp_dob = models.DateField(blank=True, null=True)
    emp_address = models.CharField(max_length=1000, blank=True, null=True)
    emp_nric = models.BigIntegerField(blank=True, null=True)
    emp_phone_num = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'employee'
        unique_together = (('emp_name', 'emp_nric', 'emp_phone_num'),)

class EmployeeBankAccount(models.Model):
    bank_acc_id = models.BigAutoField(primary_key=True)
    bank_name = models.CharField(max_length=150, blank=True, null=True)
    bank_acc_num = models.BigIntegerField(blank=True, null=True)
    bank_acc_type = models.CharField(max_length=100, blank=True, null=True)
    bank_routing_num = models.IntegerField(blank=True, null=True)
    emp = models.ForeignKey(Employee, on_delete=models.PROTECT)

    class Meta:
        db_table = 'employee_bank_account'
        unique_together = (('bank_acc_num', 'emp'),)

class EmployeeBenefitAccount(models.Model):
    benefit_acc_id = models.BigAutoField(primary_key=True)
    benefit_acc_name = models.CharField(max_length=150)
    benefit_acc_type = models.CharField(max_length=100, blank=True, null=True)
    benefit_acc_num = models.BigIntegerField()
    emp = models.ForeignKey(Employee, on_delete=models.PROTECT)

    class Meta:
        db_table = 'employee_benefit_account'
        unique_together = (('emp', 'benefit_acc_num'),)