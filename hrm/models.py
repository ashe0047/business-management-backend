from django.db import models


class Employee(models.Model):
    emp_id = models.IntegerField(primary_key=True)
    emp_name = models.CharField(max_length=150, blank=True, null=True)
    emp_dob = models.DateField(blank=True, null=True)
    emp_address = models.CharField(max_length=1000, blank=True, null=True)
    emp_nric = models.IntegerField(blank=True, null=True)
    empy_phone_num = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'employee'

class EmpBankAccount(models.Model):
    bank_acc_id = models.IntegerField(primary_key=True)
    bank_name = models.CharField(max_length=150, blank=True, null=True)
    bank_acc_num = models.IntegerField(blank=True, null=True)
    bank_acc_type = models.CharField(max_length=100, blank=True, null=True)
    bank_routing_num = models.IntegerField(blank=True, null=True)
    emp = models.ForeignKey(Employee, on_delete=models.PROTECT)

    class Meta:
        db_table = 'emp_bank_account'
        unique_together = (('bank_acc_num', 'emp', 'bank_acc_id'),)

class EmployeeBenefitAccount(models.Model):
    benefit_acc_id = models.IntegerField(primary_key=True)
    benefit_acc_name = models.CharField(max_length=150)
    benefit_acc_type = models.CharField(max_length=100, blank=True, null=True)
    benefit_acc_num = models.IntegerField()
    emp = models.ForeignKey(Employee, on_delete=models.PROTECT)

    class Meta:
        db_table = 'employee_benefit_account'
        unique_together = (('benefit_acc_id', 'emp', 'benefit_acc_num'),)