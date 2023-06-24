from typing import Any, Dict, Tuple
from django.db import models
from django.core.exceptions import ValidationError
from crm.models import Customer
from inventory.models import Product, Service, ServicePackage, ServicePackageService
from marketing.models import *
class Sale(models.Model):
    sales_id = models.BigAutoField(primary_key=True)
    cust = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=False, null=False, related_name='sale')
    sales_datetime = models.DateTimeField(auto_now_add=True,blank=False, null=False)
    sales_total_amt = models.DecimalField(max_digits=1000, decimal_places=10, blank=False, null=False)
    gen_voucher_used = models.ManyToManyField(Voucher, related_name='sale', through="VoucherUsage") #Generic voucher used
    sales_payment_type = models.CharField(max_length=100, blank=False, null=False)
    
    def clean(self):
        if not isinstance(self.gen_voucher_used, GenericVoucher):
            raise ValidationError('Voucher type is not valid')
        super().clean()
        
    class Meta:
        db_table = 'sale'

class PackageSubscription(models.Model):
    pkg_sub_id = models.BigAutoField(primary_key=True)
    pkg = models.ForeignKey(ServicePackage, on_delete=models.PROTECT, related_name='packagesubscription')
    cust = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='packagesubscription')
    service = models.ManyToManyField(Service, related_name='packagesubscription', through='PackageSubscriptionService')
    paid_amt = models.DecimalField(max_digits=1000, decimal_places=10, default=0)
    remaining_balance = models.DecimalField(max_digits=1000, decimal_places=10)
    fully_paid = models.BooleanField(default=False)

    #Deletion of package subscription instance must be accompanied by delete of all related instance in packagesubscriptionservice
    def delete(self, using=None, keep_parents=False):
        #delete all related entry in PackageSubscriptionService Junction table
        self.service.clear()

        return super().delete(using, keep_parents)
    
    def save(self, *args, **kwargs):
        not_created = not self.pkg_sub_id
        self.remaining_balance = self.pkg.pkg_price - self.paid_amt
        self.fully_paid = True if self.remaining_balance == 0 else False
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

# #To track multiple generic voucher used in sale
class VoucherUsage(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.PROTECT, blank=False, null=False, related_name='voucherusage')
    sales = models.ForeignKey("pos.Sale", on_delete=models.PROTECT, blank=False, null=False, related_name='voucherusage')

class SaleItem(models.Model):
    sales_item_id = models.BigAutoField(primary_key=True)
    sales = models.ForeignKey(Sale, on_delete=models.PROTECT, related_name='saleitem')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, blank=True, null=True, related_name='saleitem')
    pkg_sub = models.ForeignKey(PackageSubscription, on_delete=models.PROTECT, blank=True, null=True, related_name='saleitem')
    prod = models.ForeignKey(Product, on_delete=models.PROTECT, blank=True, null=True, related_name='saleitem')
    voucher = models.ForeignKey(Voucher, on_delete=models.PROTECT, blank=True, null=True, related_name='saleitem_buy')
    cat_item_voucher = models.ForeignKey(Voucher, on_delete=models.PROTECT, blank=True, null=True, related_name='saleitem_use') #category/item specific voucher
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

        if not isinstance(self.voucher, (CategoryVoucher, ItemVoucher)):
            raise ValidationError("Voucher type is not valid")
        
        #check if saleitem is discounted
        inventory_field_names = ['service', 'pkg_sub', 'prod', 'voucher']
        for field_name in inventory_field_names:
            field = getattr(self, field_name)
            if field:
                if field_name == inventory_field_names[1]:
                    discount_field = field.pkg.pkg_discount_percent
                    if discount_field:
                        raise ValidationError('Voucher cannot be used on items with discounts')
                else:
                    discount_field_name = field_name + '_discount_percent'
                    discount_field = getattr(field, discount_field_name)
                    if discount_field:
                        raise ValidationError('Voucher cannot be used on items with discounts')
        super().clean()
    
    #Ensures auto deletion of pkg_sub when sale_item is deleted, as pkg_sub is technically an extension of sale item to store extra information about a package subscription
    def delete(self, using=None, keep_parents=False):
        pkg_sub = self.pkg_sub
        ret = super().delete(using, keep_parents)
        if pkg_sub:
            pkg_sub.delete()

        return ret
    class Meta:
        db_table = 'sale_item'


    

