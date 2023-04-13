from django.db import models

class ProductSupplier(models.Model):
    supplier_id = models.BigAutoField(primary_key=True)
    supplier_name = models.CharField(max_length=300)
    supplier_contact = models.BigIntegerField(blank=True, null=True)
    supplier_addres = models.CharField(max_length=1000, blank=True, null=True)
    supplier_acc_num = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'product_supplier'
        unique_together = (('supplier_name', 'supplier_acc_num'),)

class ProductCommissionStructure(models.Model):
    prod_com_id = models.BigAutoField(primary_key=True)
    prod_com_type = models.CharField(max_length=50, blank=True, null=True, unique=True)
    prod_com_rate = models.DecimalField(max_digits=1000, decimal_places=10)

    class Meta:
        db_table = 'product_commission_structure'

class ServicecCommissionStructure(models.Model):
    service_com_id = models.BigAutoField(primary_key=True)
    service_com_type = models.CharField(max_length=50, blank=True, null=True, unique=True)
    service_com_rate = models.DecimalField(max_digits=1000, decimal_places=10)
    
    class Meta:
        db_table = 'service_commission_structure'

class Product(models.Model):
    prod_id = models.BigAutoField(primary_key=True)
    prod_name = models.CharField(max_length=300)
    prod_desc = models.TextField(blank=True, null=True)
    prod_category = models.CharField(max_length=100, blank=True, null=True)
    prod_price = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)
    prod_qty = models.IntegerField(blank=True, null=True)
    prod_img = models.BinaryField(blank=True, null=True)
    supplier = models.ForeignKey(ProductSupplier, on_delete=models.PROTECT)
    prod_com = models.ForeignKey(ProductCommissionStructure, on_delete=models.PROTECT)

    class Meta:
        db_table = 'product'
        unique_together = (('prod_name'),)

class Service(models.Model):
    service_id = models.BigAutoField(primary_key=True)
    service_name = models.CharField(max_length=300)
    service_desc = models.TextField(blank=True, null=True)
    service_category = models.CharField(max_length=100, blank=True, null=True)
    service_price = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)
    service_img = models.BinaryField(blank=True, null=True)
    service_com = models.ForeignKey(ServicecCommissionStructure, on_delete=models.PROTECT)


    class Meta:
        db_table = 'service'
        unique_together = (('service_name'),)

