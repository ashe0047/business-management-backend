from django.db import models

class ProductsSupplier(models.Model):
    supplier_id = models.IntegerField(primary_key=True)
    supplier_name = models.CharField(max_length=300)
    supplier_contact = models.BigIntegerField(blank=True, null=True)
    supplier_addres = models.CharField(max_length=1000, blank=True, null=True)
    supplier_acc_num = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'products_supplier'
        
class Products(models.Model):
    prod_id = models.IntegerField(primary_key=True)
    prod_name = models.CharField(max_length=300)
    prod_desc = models.TextField(blank=True, null=True)
    prod_category = models.CharField(max_length=100, blank=True, null=True)
    prod_price = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)
    prod_qty = models.IntegerField(blank=True, null=True)
    prod_img = models.BinaryField(blank=True, null=True)
    supplier = models.ForeignKey(ProductsSupplier, on_delete=models.PROTECT)

    class Meta:
        db_table = 'products'
        unique_together = (('prod_id', 'supplier'),)

class Services(models.Model):
    service_id = models.IntegerField(primary_key=True)
    service_name = models.CharField(max_length=300)
    service_desc = models.TextField(blank=True, null=True)
    service_category = models.CharField(max_length=100, blank=True, null=True)
    service_price = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)
    service_img = models.BinaryField(blank=True, null=True)

    class Meta:
        db_table = 'services'