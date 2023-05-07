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
    
class Product(models.Model):
    prod_id = models.BigAutoField(primary_key=True)
    prod_name = models.CharField(max_length=300)
    prod_desc = models.TextField(blank=True, null=True)
    prod_category = models.CharField(max_length=100, blank=True, null=True)
    prod_price = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)
    prod_qty = models.IntegerField(blank=True, null=True)
    prod_img = models.BinaryField(blank=True, null=True)
    supplier = models.ForeignKey(ProductSupplier, on_delete=models.PROTECT)
    prod_com = models.ForeignKey('core.ProductCommissionStructure', on_delete=models.PROTECT)

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
    service_com = models.ForeignKey('core.ServiceCommissionStructure', on_delete=models.PROTECT)


    class Meta:
        db_table = 'service'
        unique_together = (('service_name'),)

class ServicePackage(models.Model):
    pkg_id = models.BigAutoField(primary_key=True)
    pkg_name = models.CharField(max_length=300)
    pkg_desc = models.TextField(blank=True, null=True)
    pkg_category = models.CharField(max_length=100, blank=True, null=True)
    pkg_price = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)
    pkg_img = models.BinaryField(blank=True, null=True)
    service = models.ManyToManyField(Service, related_name='service', through='ServicePackageService')

    class Meta:
        db_table = 'service_package'
        unique_together = (('pkg_name', ))

class ServicePackageService(models.Model): #Junction table to store the information regarding each service in each package
    sps_id = models.BigAutoField(primary_key=True)
    pkg = models.ForeignKey(ServicePackage, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    num_treatments = models.IntegerField(default=1)

    class Meta:
        db_table = 'service_package_service'

