from django.db import models
from hrm.models import *
from inventory.models import *


class Customer(models.Model):
    CUST_SOURCE = (
        ('advertisement', 'Advertisement'),
        ('referral', 'Referral'),
        ('online_search', 'Online Search'),
        ('social_media', 'Social Media'),
        ('word_of_mouth', 'Word of Mouth'),
        ('event', 'Event'),
        ('newspaper', 'Newspaper'),
        ('television', 'Television'),
        ('radio', 'Radio'),
        ('email_marketing', 'Email Marketing'),
        ('direct_mail', 'Direct Mail'),
        ('other', 'Other'),
    )
    cust_id = models.BigAutoField(primary_key=True)
    cust_name = models.CharField(max_length=150)
    cust_phone_num = models.BigIntegerField()
    cust_address = models.CharField(max_length=1000, blank=True, null=True)
    cust_dob = models.DateField(blank=True, null=True)
    cust_email = models.CharField(max_length=300, blank=True, null=True)
    cust_nric = models.BigIntegerField()
    cust_occupation = models.CharField(max_length=300, blank=True, null=True)
    cust_source = models.CharField(max_length=30, choices=CUST_SOURCE, blank=True, null=True) #fixed choices
    cust_med_hist = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'customer'
        unique_together = (('cust_phone_num', 'cust_nric', 'cust_name', 'cust_email'),)


class Treatment(models.Model):
    cust = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='treatment')
    emp = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='treatment')
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    pkg_sub = models.ForeignKey('pos.PackageSubscription', on_delete=models.PROTECT)
    treatment_date = models.DateTimeField()
    treatment_notes = models.TextField(blank=True)
    treatment_img = models.ImageField()

    class Meta:
        db_table = 'treatment'