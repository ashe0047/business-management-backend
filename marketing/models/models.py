from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from crm.models.models import Customer
from inventory.models import *
from config.utils import get_config_value, update_config_value
from config.enums import ConfigKeys

# Create your models here.
class Voucher(models.Model):
    VOUCHER_TYPES = [
        ('discount', 'Discount Voucher'),
        ('gift', 'Gift Voucher'),
        ('promo', 'Promotional Voucher'),
    ]

    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    #auto voucher code generator
    def voucher_code_generator():
        code_prefix = get_config_value(ConfigKeys.VOUCHER_CODE_PREFIX.value)
        last_sequence = get_config_value(ConfigKeys.VOUCHER_LATEST_CODE.value)
        new_sequence = int(last_sequence) + 1
        
        return code_prefix + f'{str(new_sequence).zfill(4)}'
    
    voucher_id = models.BigAutoField(primary_key=True)
    voucher_code = models.CharField(max_length=100, unique=True, blank=True, null=True, default=voucher_code_generator)
    voucher_name = models.CharField(max_length=255)
    voucher_desc = models.TextField(blank=True, null=True)
    voucher_type = models.CharField(max_length=20, choices=VOUCHER_TYPES)
    voucher_discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    voucher_start_date = models.DateField(blank=True, null=True)
    voucher_end_date = models.DateField(blank=True, null=True)
    voucher_created_date = models.DateTimeField(auto_now_add=True)
    voucher_sale_price = models.DecimalField(max_digits=1000, decimal_places=10)
    voucher_sale_discount_percent = models.DecimalField(max_digits=1000, decimal_places=10, default=0)
    voucher_use_discount_percent = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    voucher_use_discount_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    voucher_usage_limit = models.PositiveIntegerField(blank=True, null=True)
    voucher_user_limit = models.PositiveIntegerField(blank=True, null=True)
    cust = models.ManyToManyField(Customer, blank=True)
    voucher_conditions = models.TextField(blank=True)
    voucher_redemption_count = models.PositiveIntegerField(default=0)
    voucher_com = models.ForeignKey('core.VoucherCommissionStructure', on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    
    #generates a voucher code automatically everytime an instance is created
    def save(self, *args, **kwargs):
        update_config_value(ConfigKeys.VOUCHER_LATEST_CODE.value, int(self.voucher_code[2:]))

        super().save(*args, **kwargs)

    @property
    def no_usage_limit(self):
        return self.voucher_usage_limit is None
    
    @property
    def voucher_sale_discount_amt(self):
        return self.voucher_sale_discount_percent * self.voucher_sale_price
    
    @property
    def voucher_sale_discount_price(self):
        return self.voucher_sale_price - (self.voucher_sale_discount_amt)
    
    @property
    def voucher_usage_left(self):
        pass
    
    @property
    def voucher_redeemable(self):
        return self.voucher_usage_left > 0 if not self.no_usage_limit else self.no_usage_limit

    @property
    def voucher_info(self):
        info = {
            'discount_type': self.voucher_discount_type
        }
        if self.voucher_use_discount_amt is not None:
            info.update({'discount_amt': self.voucher_use_discount_amt})
        else:
            info.update({'discount_percent': self.voucher_use_discount_percent})
        
        return info
    class Meta:
        abstract = True
        

class GenericVoucher(Voucher):

    @property
    def voucher_usage_left(self):
        return self.voucher_usage_limit - len(self.voucherusage.all()) if not self.no_usage_limit else None
    
    class Meta:
        db_table = 'generic_voucher'
        unique_together = (('voucher_code',), ('voucher_name',), )

class CategoryVoucher(Voucher):
    category = models.ForeignKey(InventoryCategory, on_delete=models.PROTECT, blank=False, null=False, related_name='categoryvoucher')
    saleitem_sale = GenericRelation('pos.SaleItem', 'voucher_sale_id', 'voucher_sale_type')
    saleitem_use = GenericRelation('pos.SaleItem', 'voucher_use_id', 'voucher_use_type')

    @property
    def voucher_usage_left(self):
            return (self.voucher_usage_limit - self.voucher_redemption_count) if not self.no_usage_limit else None
    
    class Meta:
        db_table = 'category_voucher'
        unique_together = (('voucher_code',), ('voucher_name',), )
        
class ItemVoucher(Voucher):
    prod = models.ManyToManyField(Product, blank=True, related_name='itemvoucher')
    service = models.ManyToManyField(Service, blank=True, related_name='itemvoucher')
    pkg = models.ManyToManyField(ServicePackage, blank=True, related_name='itemvoucher')
    saleitem_sale = GenericRelation('pos.SaleItem', 'voucher_sale_id', 'voucher_sale_type')
    saleitem_use = GenericRelation('pos.SaleItem', 'voucher_use_id', 'voucher_use_type')

    @property
    def voucher_usage_left(self):
        return (self.voucher_usage_limit - self.voucher_redemption_count) if not self.no_usage_limit else None
    
    @property
    def inventory_item_info(self):
        inventory_field_names = ['service', 'pkg', 'prod']
        for field_name in inventory_field_names:
            instances = getattr(self, field_name).all()
            if instances:
                return {'instances': instances, 'field_name': field_name}
            
    class Meta:
        db_table = 'item_voucher'
        unique_together = (('voucher_code',), ('voucher_name',), )