from typing import Any, Dict, Iterable, Optional, Tuple
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from crm.models.models import Customer
from inventory.models import Product, Service, ServicePackage, ServicePackageService
from marketing.models.models import *
from pos.utils import voucher_discount_amount

class Sale(models.Model):
    sales_id = models.BigAutoField(primary_key=True)
    cust = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=False, null=False, related_name='sale')
    sales_datetime = models.DateTimeField(auto_now_add=True,blank=False, null=False)
    gross_sales_amt = models.DecimalField(max_digits=1000, decimal_places=2, blank=True, null=True)
    net_sales_amt = models.DecimalField(max_digits=1000, decimal_places=2, blank=True, null=True)
    gen_voucher_use = models.ManyToManyField(GenericVoucher, related_name='sale', through="VoucherUsage") #Generic voucher used
    sales_payment_method = models.CharField(max_length=100, blank=False, null=False)
    
    
    def auto_sales_amount(self):
        #sum the gross and net sales amount for all saleitems
        self.gross_sales_amt, self.net_sales_amt = tuple(sum(values)for values in zip(*[(item.gross_sales_item_total_price, item.net_sales_item_total_price) for item in self.saleitem.all()]))

        total_discount_amt = 0
        total_discount_percent = 0
        #deduct the voucher amount from net sales amount accordingly if vouchers are used
        if len(self.gen_voucher_use.all()) != 0:
            for voucher in self.gen_voucher_use.all():
                if voucher.voucher_info['discount_type'] == 'percentage':
                    total_discount_percent += voucher.voucher_info['discount_percent']
                else:
                    total_discount_amt += voucher.voucher_info['discount_amt']
            self.net_sales_amt = self.net_sales_amt - (total_discount_percent*self.net_sales_amt) - total_discount_amt

    
    def save(self, *args, **kwargs):
        #unpack and sum up the values for gross and net amount for all saleitem and assign to sales
        if self.sales_id: 
            self.auto_sales_amount()
        
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'sale'

# #To track multiple generic voucher used in sale
class VoucherUsage(models.Model):
    voucher = models.ForeignKey(GenericVoucher, on_delete=models.PROTECT, blank=False, null=False, related_name='voucherusage')
    sales = models.ForeignKey("pos.Sale", on_delete=models.PROTECT, blank=False, null=False, related_name='voucherusage')

    class Meta:
        db_table = 'voucher_usage'
        unique_together = (('voucher','sales',),)

class PackageSubscription(models.Model):
    pkg_sub_id = models.BigAutoField(primary_key=True)
    pkg = models.ForeignKey(ServicePackage, on_delete=models.PROTECT, related_name='packagesubscription')
    cust = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='packagesubscription')
    service = models.ManyToManyField(Service, related_name='packagesubscription', through='PackageSubscriptionService')
    paid_amt = models.DecimalField(max_digits=1000, decimal_places=10, default=0)
    remaining_balance = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)
    fully_paid = models.BooleanField(default=False)

    #Deletion of package subscription instance must be accompanied by delete of all related instance in packagesubscriptionservice
    def delete(self, using=None, keep_parents=False):
        #delete all related entry in PackageSubscriptionService Junction table
        self.service.clear()

        return super().delete(using, keep_parents)
    
    def save(self, *args, **kwargs):
        not_created = not self.pkg_sub_id
        self.remaining_balance = (self.pkg.pkg_price if self.pkg.pkg_discount_percent is None else self.pkg.pkg_discount_price) - self.paid_amt
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
        unique_together = (('pkg_sub','service',),)
        
class SaleItem(models.Model):
    # Define the allowed content types
    ALLOWED_VOUCHER_USE_TYPES = [
        'genericvoucher',
        'itemvoucher',
        'categoryvoucher',
    ]

    ALLOWED_VOUCHER_SALE_TYPES = [
        'itemvoucher',
        'categoryvoucher',
    ]
    sales_item_id = models.BigAutoField(primary_key=True)
    sales = models.ForeignKey(Sale, on_delete=models.PROTECT, related_name='saleitem')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, blank=True, null=True, related_name='saleitem')
    #1:M Multiple saleitem can be linked to pkg_sub for subsequent payments of remaining balance
    pkg_sub = models.ForeignKey(PackageSubscription, on_delete=models.PROTECT, blank=True, null=True, related_name='saleitem')
    prod = models.ForeignKey(Product, on_delete=models.PROTECT, blank=True, null=True, related_name='saleitem')

    voucher_sale_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True, related_name='saleitem_sale', limit_choices_to={'model__in': ALLOWED_VOUCHER_SALE_TYPES})
    voucher_sale_id = models.PositiveIntegerField(blank=True, null=True)
    voucher_sale = GenericForeignKey('voucher_sale_type', 'voucher_sale_id')
    # voucher = models.ForeignKey(Voucher, on_delete=models.PROTECT, blank=True, null=True, related_name='saleitem_sale')
    # cat_item_voucher = models.ForeignKey(Voucher, on_delete=models.PROTECT, blank=True, null=True, related_name='saleitem_use') #category/item specific voucher
    
    voucher_use_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True, related_name='saleitem_use', limit_choices_to={'model__in': ALLOWED_VOUCHER_USE_TYPES})
    voucher_use_id = models.PositiveIntegerField(blank=True, null=True)
    voucher_use = GenericForeignKey('voucher_use_type', 'voucher_use_id') #category/item specific voucher
    
    sale_item_type = models.CharField(max_length=50, blank=True, null=True)
    sales_item_qty = models.IntegerField(blank=True, null=True)
    gross_sales_item_unit_price = models.DecimalField(max_digits=1000, decimal_places=2)
    net_sales_item_unit_price = models.DecimalField(max_digits=1000, decimal_places=2)
    gross_sales_item_total_price = models.DecimalField(max_digits=1000, decimal_places=2)
    net_sales_item_total_price = models.DecimalField(max_digits=1000, decimal_places=2)
    

    @property
    def inventory_item_info(self):
        inventory_field_names = ['service', 'pkg_sub', 'prod', 'voucher_sale']
        for field_name in inventory_field_names:
            instance = getattr(self, field_name)
            if instance:
                return {'instance': instance, 'field_name': field_name}
            
    @property
    def voucher_use_discount_amount(self):
        if self.voucher_use:
            if self.voucher_use.voucher_info['discount_type'] == 'percentage':
                inventory_item = self.inventory_item_info['instance']
                inventory_item_price_field_name = self.inventory_item_info['field_name'] + '_price'
                inventory_item_price = getattr(inventory_item, inventory_item_price_field_name)
                return self.voucher_use.voucher_info['discount_percent'] * inventory_item_price
            else:
                return self.voucher_use.voucher_info['discount_amt']
        return 0 
    
    def auto_sale_item_prices(self):
        #automatic retrieval of gross_sales_item_price from inventory fields
        inventory_field_names = ['service', 'pkg_sub', 'prod', 'voucher_sale']
        inventory_field = self.inventory_item_info['instance']
        inventory_field_name = self.inventory_item_info['field_name']
        if inventory_field_name == inventory_field_names[1]:
            price_field = inventory_field.pkg.pkg_price
            discount_price_field = inventory_field.pkg.pkg_discount_price
            self.gross_sales_item_unit_price = price_field
            self.net_sales_item_unit_price = discount_price_field if self.voucher_use is None else (discount_price_field - self.voucher_use_discount_amount)  
        elif inventory_field_name == inventory_field_names[-1]:
            price_field = inventory_field.voucher_sale_price
            discount_price_field = inventory_field.voucher_sale_discount_price
            self.gross_sales_item_unit_price = price_field
            self.net_sales_item_unit_price = discount_price_field 
        else:
            price_field_name = inventory_field_name + '_price'
            discount_price_field_name = inventory_field_name + '_discount_price'
            price_field = getattr(inventory_field, price_field_name)
            discount_price_field = getattr(inventory_field, discount_price_field_name)
            self.gross_sales_item_unit_price = price_field
            self.net_sales_item_unit_price = discount_price_field if self.voucher_use is None else (discount_price_field - self.voucher_use_discount_amount)
        #calculate total prices for the qty
        self.gross_sales_item_total_price = self.gross_sales_item_unit_price * self.sales_item_qty
        self.net_sales_item_total_price = self.net_sales_item_unit_price * self.sales_item_qty

    #Ensures auto deletion of pkg_sub when sale_item is deleted, as pkg_sub is technically an extension of sale item to store extra information about a package subscription
    def delete(self, using=None, keep_parents=False):
        pkg_sub = self.pkg_sub
        ret = super().delete(using, keep_parents)
        if pkg_sub:
            pkg_sub.delete()
        return ret
    
    def save(self, *args, **kwargs):
        # auto filling in of sales_item_price for gross and net
        self.auto_sale_item_prices()

        super().save(*args, **kwargs)


    class Meta:
        db_table = 'sale_item'


    

