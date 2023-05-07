from django.db import models
from hrm.models import *
from inventory.models import *

class Customer(models.Model):
    cust_id = models.BigAutoField(primary_key=True)
    cust_name = models.CharField(max_length=150)
    cust_phone_num = models.BigIntegerField(blank=True, null=True)
    cust_address = models.CharField(max_length=1000, blank=True, null=True)
    cust_dob = models.DateField(blank=True, null=True)
    cust_email = models.CharField(max_length=300, blank=True, null=True)
    cust_nric = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'customer'
        unique_together = (('cust_phone_num', 'cust_nric', 'cust_name', 'cust_email'),)


class Treatment(models.Model):
    cust = models.ForeignKey(Customer, on_delete=models.PROTECT)
    emp = models.ForeignKey(Employee, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    pkg_sub = models.ForeignKey('pos.PackageSubscription', on_delete=models.PROTECT)
    treatment_date = models.DateTimeField()
    treatment_notes = models.TextField(blank=True)
    treatment_img = models.ImageField()

    class Meta:
        db_table = 'treatment'