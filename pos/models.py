from typing import Any, Dict, Tuple
from django.db import models
from django.core.exceptions import ValidationError
from crm.models import Customer
from inventory.models import Product, Service, ServicePackage, ServicePackageService

class Sale(models.Model):
    sales_id = models.BigAutoField(primary_key=True)
    cust = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True, related_name='customer')
    sales_datetime = models.DateTimeField(auto_now_add=True,blank=False, null=False)
    sales_total_amt = models.DecimalField(max_digits=1000, decimal_places=10, blank=False, null=False)
    sales_payment_type = models.CharField(max_length=100, blank=False, null=False)
    
    class Meta:
        db_table = 'sale'

class PackageSubscription(models.Model):
    pkg_sub_id = models.BigAutoField(primary_key=True)
    pkg = models.ForeignKey(ServicePackage, on_delete=models.PROTECT, related_name='packagesubscription')
    cust = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='packagesubscription')
    service = models.ManyToManyField(Service, related_name='packagesubscription', through='PackageSubscriptionService')
    deposit_amt = models.DecimalField(max_digits=1000, decimal_places=10)

    #Deletion of package subscription instance must be accompanied by delete of all related instance in packagesubscriptionservice
    def delete(self, using=None, keep_parents=False):
        #delete all related entry in PackageSubscriptionService Junction table
        self.service.clear()

        return super().delete(using, keep_parents)
    
    def save(self, *args, **kwargs):
        not_created = not self.pkg_sub_id
        super().save(*args, **kwargs)
        
        #automatically populate the services that are related to the servicepackage in this subscription and the default num_treatment
        if not_created:
            service_package_services = ServicePackageService.objects.filter(pkg=self.pkg)

            for service_package_service in service_package_services:
                num_treatments = service_package_service.num_treatments
                package_subscription_service = PackageSubscriptionService.objects.create(
                    pkg_sub=self,
                    service=service_package_service.service,
                    treatment_left=num_treatments
                )

    class Meta:
        db_table = 'package_subscription'

class PackageSubscriptionService(models.Model): #Junction table to track the number of treatments left for each packagesubscription and each service
    pkg_sub_service_id = models.BigAutoField(primary_key=True)
    pkg_sub = models.ForeignKey(PackageSubscription, on_delete=models.PROTECT, related_name='packagesubscriptionservice')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='packagesubscriptionservice')
    treatment_left = models.IntegerField(null=False)

    class Meta:
        db_table = 'package_subscription_service'

class SaleItem(models.Model):
    sales_item_id = models.BigAutoField(primary_key=True)
    sales = models.ForeignKey(Sale, on_delete=models.PROTECT, related_name='saleitem')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, blank=True, null=True, related_name='saleitem')
    pkg_sub = models.ForeignKey(PackageSubscription, on_delete=models.PROTECT, blank=True, null=True, related_name='saleitem')
    prod = models.ForeignKey(Product, on_delete=models.PROTECT, blank=True, null=True, related_name='saleitem')
    sale_item_type = models.CharField(max_length=50, blank=True, null=True)
    sales_item_qty = models.IntegerField(blank=True, null=True)
    sales_item_price = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)

    #Validation for assigning only one of service,product or package subscription to a single sale item instance
    def clean(self):
        if self.service and (self.pkg_sub or self.prod):
            raise ValidationError("Only one of service,prod or pkg_sub field can have a value.")
        
        if self.pkg_sub and (self.service or self.prod):
            raise ValidationError("Only one of service,prod or pkg_sub field can have a value.")
        
        if self.prod and (self.service or self.pkg_sub):
            raise ValidationError("Only one of service,prod or pkg_sub field can have a value.")

        super().clean()
    
    class Meta:
        db_table = 'sale_item'


    

