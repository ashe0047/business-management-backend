from django.db import models
from django.core.exceptions import ValidationError
from gdstorage.storage import GoogleDriveStorage
from inventory.utils import sku_generator


gd_storage = GoogleDriveStorage()

def upload_to_handler(instance, filename):
    ext = filename.split('.')[-1]
    if isinstance(instance, Product):
        sku = instance.prod_sku
    return f"inventory/products/{sku}.{ext}"

class ProductSupplier(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300)
    contact = models.BigIntegerField(blank=True, null=True)
    addres = models.CharField(max_length=1000, blank=True, null=True)
    acc_num = models.BigIntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = 'product_supplier'
        unique_together = (('name', 'acc_num',),)

class ProductBrand(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150, null=False, blank=False)
    desc = models.CharField(max_length=300, null=True, blank=True)
    origin_country = models.CharField(max_length=100, null=True, blank=True)
    ext_info = models.FileField(upload_to='inventory/products/brand/docs', storage=gd_storage, null=True, blank=True)
    sku_part = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = 'product_brand'
        unique_together = (('name',), ('sku_part',),)

# Weight/Volume of product
class ProductUnitSize(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    unit = models.CharField(max_length=25)
    sku_part = models.CharField(max_length=10, null=False, blank=False)
    
    def __str__(self) -> str:
        return str(self.value)+self.unit
    class Meta:
        db_table = 'product_unit_size'
        unique_together = (('value', 'unit',), ('sku_part',),)

class ProductPackageSize(models.Model):
    id = models.BigAutoField(primary_key=True)
    qty = models.IntegerField(blank=False, null=False)
    unit = models.CharField(max_length=25)
    sku_part = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self) -> str:
        return str(self.qty)+'/'+self.unit
    
    class Meta:
        db_table = 'product_package_size'
        unique_together = (('qty', 'unit',), ('sku_part',),)

class ProductWeight(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    unit = models.CharField(max_length=25)
    sku_part = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self) -> str:
        return str(self.value)+self.unit
    class Meta:
        db_table = 'product_weight'
        unique_together = (('value', 'unit',), ('sku_part',),)

class ProductVariant(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150, null=False, blank=False)
    sku_part = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = 'product_variant'
        unique_together = (('name',), ('sku_part',),)

class Product(models.Model):

    prod_id = models.BigAutoField(primary_key=True)
    prod_brand = models.ForeignKey(ProductBrand, on_delete=models.PROTECT, related_name='product', null=False, blank=False)
    prod_name = models.CharField(max_length=300, blank=False, null=False)
    prod_desc = models.TextField(blank=True, null=True)
    prod_category = models.ForeignKey("inventory.InventoryCategory", on_delete=models.PROTECT, related_name='product', null=False, blank=False)
    prod_variant = models.ForeignKey(ProductVariant, related_name='product', on_delete=models.PROTECT, null=True, blank=True)
    prod_unit_size = models.ForeignKey(ProductUnitSize, related_name='product', on_delete=models.PROTECT, null=True, blank=True)
    prod_package_size = models.ForeignKey(ProductPackageSize, related_name='product', on_delete=models.PROTECT, null=True, blank=True)
    prod_weight = models.ForeignKey(ProductWeight, related_name='product', on_delete=models.PROTECT, null=True, blank=True)
    prod_ingredients = models.TextField(null=True, blank=True)
    prod_exp_date = models.DateField(null=True, blank=True)
    prod_cost = models.DecimalField(max_digits=1000, decimal_places=10, blank=False, null=False)
    prod_price = models.DecimalField(max_digits=1000, decimal_places=10, blank=False, null=False)
    prod_discount_percent = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)
    prod_qty = models.IntegerField(blank=False, null=False)
    prod_img = models.ImageField(upload_to=upload_to_handler, storage=gd_storage, blank=True, null=True)
    prod_sku = models.CharField(max_length=100, blank=True, null=True)
    prod_barcode = models.CharField(max_length=13, blank=True, null=True)
    supplier = models.ForeignKey(ProductSupplier, on_delete=models.PROTECT, related_name='product', null=True, blank=True)
    prod_com = models.ForeignKey('core.ProductCommissionStructure', on_delete=models.PROTECT, related_name='product', null=True, blank=True)
    is_active = models.BooleanField(default=True, null=False, blank=False)

    

    @property
    def prod_discount_amt(self):
        if self.prod_discount_percent:
            return self.prod_price * self.prod_discount_percent
        else:
            return 0
        
    @property
    def prod_discount_price(self):
        if self.prod_discount_percent:
            return self.prod_price - self.prod_discount_amt
        else:
            return self.prod_price

    @property
    def prod_profit_margin(self):
        margin = {
            'profit_margin': self.prod_price - self.prod_cost,
            'profit_margin_percent': (self.prod_price - self.prod_cost)/self.prod_cost
        }
        return margin

    def save(self, *args, **kwargs):
        # Assigning the generated SKU code to the prod_sku field
        self.prod_sku = sku_generator(self, 'PROD')

        return super().save(*args, **kwargs)
        

    class Meta:
        db_table = 'product'
        unique_together = (('prod_name', 'prod_category', 'prod_variant', 'prod_unit_size', 'prod_package_size', 'prod_weight',),('prod_sku',),('prod_barcode',),)

class Service(models.Model):
    service_id = models.BigAutoField(primary_key=True)
    service_name = models.CharField(max_length=300)
    service_desc = models.TextField(blank=True, null=True)
    service_category = models.ForeignKey("inventory.InventoryCategory", on_delete=models.PROTECT, related_name='service', null=False, blank=False)
    service_price = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)
    service_discount_percent = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)
    service_img = models.ImageField(upload_to='inventory/products', storage=gd_storage, blank=True, null=True)
    service_com = models.ForeignKey('core.ServiceCommissionStructure', on_delete=models.PROTECT, related_name='service', null=True, blank=True)
    is_active = models.BooleanField(default=True, null=False, blank=False)

    @property
    def service_discount_amt(self):
        if self.service_discount_percent:
            return self.service_price * self.service_discount_percent
        else:
            return 0
        
    @property
    def service_discount_price(self):
        if self.service_discount_percent:
            return self.service_price - self.service_discount_amt
        else:
            return self.service_price

    
    class Meta:
        db_table = 'service'
        unique_together = (('service_name',),)

class ServicePackage(models.Model):
    pkg_id = models.BigAutoField(primary_key=True)
    pkg_name = models.CharField(max_length=300, blank=False, null=False)
    pkg_desc = models.TextField(blank=True, null=True)
    pkg_category = models.ForeignKey("inventory.InventoryCategory", on_delete=models.PROTECT, related_name='servicepackage', null=False, blank=False)
    pkg_price = models.DecimalField(max_digits=1000, decimal_places=10, blank=False, null=False)
    pkg_discount_percent = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True) 
    pkg_img = models.ImageField(upload_to='inventory/products', storage=gd_storage, blank=True, null=True)
    service = models.ManyToManyField(Service, related_name='servicepackage', through='ServicePackageService')
    is_active = models.BooleanField(default=True, null=False, blank=False)

    @property
    def pkg_discount_amt(self):
        if self.pkg_discount_percent:
            return self.pkg_price * self.pkg_discount_percent
        else:
            return 0
        
    @property
    def pkg_discount_price(self):
        if self.pkg_discount_percent:
            return self.pkg_price - self.pkg_discount_amt
        else:
            return self.pkg_price
    
    class Meta:
        db_table = 'service_package'
        unique_together = (('pkg_name', ),)

class ServicePackageService(models.Model): #Junction table to store the information regarding each service in each package
    sps_id = models.BigAutoField(primary_key=True)
    pkg = models.ForeignKey(ServicePackage, on_delete=models.PROTECT, related_name='servicepackageservice', null=False, blank=False)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='servicepackageservice', null=False, blank=False)
    num_treatments = models.IntegerField(default=1)

    class Meta:
        db_table = 'service_package_service'
        unique_together = (('pkg','service',),)

class InventoryCategory(models.Model):
    INVENTORY_TYPES = [
        ('product', 'Product'),
        ('service', 'Service'),
        ('servicepackage', 'Service Package')
    ]
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=15, choices=INVENTORY_TYPES)
    name = models.CharField(max_length=30, null=False, blank=False)
    sku_part = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = 'inventory_category'
        verbose_name_plural = 'Inventory Categories'
        unique_together = (('name',), ('sku_part',),)