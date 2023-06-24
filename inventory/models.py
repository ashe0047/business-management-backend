from django.db import models
from django.core.exceptions import ValidationError

class ProductSupplier(models.Model):
    supplier_id = models.BigAutoField(primary_key=True)
    supplier_name = models.CharField(max_length=300)
    supplier_contact = models.BigIntegerField(blank=True, null=True)
    supplier_addres = models.CharField(max_length=1000, blank=True, null=True)
    supplier_acc_num = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'product_supplier'
        unique_together = (('supplier_name', 'supplier_acc_num'),)
    
class Product(models.Model):
    prod_id = models.BigAutoField(primary_key=True)
    prod_name = models.CharField(max_length=300, blank=False, null=False)
    prod_desc = models.TextField(blank=True, null=True)
    prod_category = models.ForeignKey("inventory.InventoryCategory", on_delete=models.PROTECT, related_name='product', null=False, blank=False)
    prod_cost = models.DecimalField(max_digits=1000, decimal_places=10, blank=False, null=False)
    prod_price = models.DecimalField(max_digits=1000, decimal_places=10, blank=False, null=False)
    prod_discount_percent = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)
    prod_qty = models.IntegerField(blank=False, null=False)
    prod_img = models.BinaryField(blank=True, null=True)
    prod_sku = models.CharField(max_length=13, unique=True, blank=True, null=True)
    prod_barcode = models.CharField(max_length=13, unique=True, blank=True, null=True)
    supplier = models.ForeignKey(ProductSupplier, on_delete=models.PROTECT, related_name='product', null=True, blank=True)
    prod_com = models.ForeignKey('core.ProductCommissionStructure', on_delete=models.PROTECT, related_name='product', null=True, blank=True)
    is_active = models.BooleanField(default=True, null=False, blank=False)

    @property
    def prod_discount_price(self):
        if self.prod_discount_percent:
            return self.prod_price - (self.prod_price * self.prod_discount_percent)
        else:
            return self.prod_price
    
    @property
    def prod_discount_amt(self):
        if self.prod_discount_percent:
            return self.prod_price * self.prod_discount_percent
        else:
            return 0

    @property
    def prod_profit_margin(self):
        margin = {
            'profit_margin': self.prod_price - self.prod_cost,
            'profit_margin_percent': (self.prod_price - self.prod_cost)/self.prod_cost
        }
        return margin
    def clean(self):
        if self.prod_discount_percent > 1 or self.prod_discount_percent < 0:
            raise ValidationError("prod_discount_percent value must be between 0 and 1")
        
        super().clean()

    class Meta:
        db_table = 'product'
        unique_together = (('prod_name'),)

class Service(models.Model):
    service_id = models.BigAutoField(primary_key=True)
    service_name = models.CharField(max_length=300)
    service_desc = models.TextField(blank=True, null=True)
    service_category = models.ForeignKey("inventory.InventoryCategory", on_delete=models.PROTECT, related_name='service', null=False, blank=False)
    service_price = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)
    service_discount_percent = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)
    service_img = models.BinaryField(blank=True, null=True)
    service_com = models.ForeignKey('core.ServiceCommissionStructure', on_delete=models.PROTECT, related_name='service', null=True, blank=True)
    is_active = models.BooleanField(default=True, null=False, blank=False)

    @property
    def service_discount_price(self):
        if self.service_discount_percent:
            return self.service_price - (self.service_price * self.service_discount_percent)
        else:
            return self.service_price
    
    @property
    def service_discount_amt(self):
        if self.service_discount_percent:
            return self.service_price * self.service_discount_percent
        else:
            return 0

    
    def clean(self):
        if self.service_discount_percent > 1 or self.service_discount_percent < 0:
            raise ValidationError("service_discount_percent value must be between 0 and 1")
        
        super().clean()
    class Meta:
        db_table = 'service'
        unique_together = (('service_name'),)

class ServicePackage(models.Model):
    pkg_id = models.BigAutoField(primary_key=True)
    pkg_name = models.CharField(max_length=300, blank=False, null=False)
    pkg_desc = models.TextField(blank=True, null=True)
    pkg_category = models.ForeignKey("inventory.InventoryCategory", on_delete=models.PROTECT, related_name='servicepackage', null=False, blank=False)
    pkg_price = models.DecimalField(max_digits=1000, decimal_places=10, blank=False, null=False)
    pkg_discount_percent = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True) 
    pkg_img = models.BinaryField(blank=True, null=True)
    service = models.ManyToManyField(Service, related_name='servicepackage', through='ServicePackageService')
    is_active = models.BooleanField(default=True, null=False, blank=False)

    @property
    def pkg_discount_price(self):
        if self.pkg_discount_percent:
            return self.pkg_price - (self.pkg_price * self.pkg_discount_percent)
        else:
            return self.pkg_price
    
    @property
    def pkg_discount_amt(self):
        if self.pkg_discount_percent:
            return self.pkg_price * self.pkg_discount_percent
        else:
            return 0
    
    def clean(self):
        if self.pkg_discount_percent > 1 or self.pkg_discount_percent < 0:
            raise ValidationError("pkg_discount_percent value must be between 0 and 1")
        
        super().clean()
    class Meta:
        db_table = 'service_package'
        unique_together = (('pkg_name', ))

class ServicePackageService(models.Model): #Junction table to store the information regarding each service in each package
    sps_id = models.BigAutoField(primary_key=True)
    pkg = models.ForeignKey(ServicePackage, on_delete=models.PROTECT, related_name='servicepackageservice', null=False, blank=False)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='servicepackageservice', null=False, blank=False)
    num_treatments = models.IntegerField(default=1)

    class Meta:
        db_table = 'service_package_service'

class InventoryCategory(models.Model):
    INVENTORY_TYPES = [
        ('product', 'Product'),
        ('service', 'Service'),
        ('servicepackage', 'Service Package')
    ]
    cat_id = models.BigAutoField(primary_key=True)
    cat_type = models.CharField(max_length=15, choices=INVENTORY_TYPES)
    cat_name = models.CharField(max_length=30, null=False, blank=False)