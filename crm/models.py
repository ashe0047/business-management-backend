from django.db import models

class Customer(models.Model):
    cust_id = models.IntegerField(primary_key=True)
    cust_name = models.CharField(max_length=150)
    cust_phone_num = models.BigIntegerField(blank=True, null=True)
    cust_address = models.CharField(max_length=1000, blank=True, null=True)
    cust_dob = models.DateField(blank=True, null=True)
    cust_email = models.CharField(max_length=300, blank=True, null=True)
    cust_nric = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'customer'
        unique_together = (('cust_id', 'cust_phone_num', 'cust_nric'),)