from django.db import models
from crm.models import Customer
from inventory.models import Product, Service, ServicePackage

class Sale(models.Model):
    sales_id = models.BigAutoField(primary_key=True)
    cust = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True)
    sales_datetime = models.DateTimeField()
    sales_total_amt = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)
    sales_payment_type = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'sale'

class PackageSubscription(models.Model):
    pkg_sub_id = models.BigAutoField(primary_key=True)
    pkg = models.ForeignKey(ServicePackage, on_delete=models.PROTECT)
    cust = models.ForeignKey(Customer, on_delete=models.PROTECT)
    deposit_amt = models.DecimalField(max_digits=1000, decimal_places=10)
    payment_datetime = models.DateTimeField()
    
    class Meta:
        db_table = 'package_subscription'

class PackageSubscriptionService(models.Model): #Junction table to track the number of treatments left for each packagesubscription and each service
    pkg_sub_service_id = models.BigAutoField(primary_key=True)
    pkg_sub = models.ForeignKey(PackageSubscription, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    treatment_left = models.IntegerField(null=False)

    class Meta:
        db_table = 'package_subscription_service'

class SaleItem(models.Model):
    sales_item_id = models.BigAutoField(primary_key=True)
    sales = models.ForeignKey(Sale, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, blank=True, null=True)
    pkg_sub = models.ForeignKey(PackageSubscription, on_delete=models.PROTECT, blank=True, null=True)
    prod = models.ForeignKey(Product, on_delete=models.PROTECT, blank=True, null=True)
    sale_item_type = models.CharField(max_length=50, blank=True, null=True)
    sales_item_qty = models.IntegerField(blank=True, null=True)
    sales_item_price = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)

    class Meta:
        db_table = 'sale_item'


    

