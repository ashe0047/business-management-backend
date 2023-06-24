from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from crm.models import Customer
from inventory.models import *


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
    voucher_id = models.BigAutoField(primary_key=True)
    voucher_code = models.CharField(max_length=100, unique=True)
    voucher_name = models.CharField(max_length=255)
    voucher_desc = models.TextField(blank=True, null=True)
    voucher_type = models.CharField(max_length=20, choices=VOUCHER_TYPES)
    voucher_discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    voucher_discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    voucher_start_date = models.DateField()
    voucher_end_date = models.DateField()
    voucher_created_date = models.DateTimeField(auto_now_add=True)
    voucher_price = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)
    voucher_discount_percent = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    voucher_discount_amt = models.DecimalField(max_digits=10, decimal_places=2)
    voucher_usage_limit = models.PositiveIntegerField()
    voucher_user_limit = models.PositiveIntegerField()
    cust = models.ManyToManyField(Customer, blank=True)
    voucher_conditions = models.TextField(blank=True)
    voucher_redemption_count = models.PositiveIntegerField(default=0)
    voucher_img = models.BinaryField(blank=True, null=True)
    voucher_com = models.ForeignKey('core.VoucherCommissionStructure', on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True, null=False, blank=False)

    #auto voucher code generator
    @staticmethod
    def voucher_code_generator():
        last_voucher = Voucher.objects.order_by('-id').first()
        if last_voucher:
            last_voucher_code = last_voucher.voucher_code
            last_sequence = int(last_voucher_code[2:])
            new_sequence = last_sequence + 1
            return f'SB{str(new_sequence).zfill(4)}'
        else:
            return 'SB0001'
    
    #generates a voucher code automatically everytime an instance is created
    def save(self, *args, **kwargs):
        if not self.voucher_code:
            self.voucher_code = self.voucher_code_generator()
        super().save(*args, **kwargs)

    #Validation for assigning only one of service,product or package subscription to a single sale item instance
    def clean(self):
        if self.voucher_discount_percent > 1 or self.voucher_discount_percent < 0:
            raise ValidationError("voucher_discount_percent value must be between 0 and 1")
        
        super().clean()

    @property
    def voucher_usage_left(self):
        return self.voucher_usage_limit - len(self.voucherusage.all())
    
    class Meta:
        db_table = 'voucher'
        
class GenericVoucher(Voucher):
    class Meta:
        db_table = 'generic_voucher'

class CategoryVoucher(Voucher):
    category = models.ForeignKey(InventoryCategory, on_delete=models.PROTECT, blank=False, null=False, related_name='categoryvoucher')

    class Meta:
        db_table = 'category_voucher'

class ItemVoucher(Voucher):
    prod = models.ManyToManyField(Product, blank=True, related_name='itemvoucher')
    service = models.ManyToManyField(Service, blank=True, related_name='itemvoucher')
    pkg = models.ManyToManyField(ServicePackage, blank=True, related_name='itemvoucher')
    
    class Meta:
        db_table = 'item_voucher'