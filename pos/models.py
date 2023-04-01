from django.db import models
from crm.models import Customer
from inventory.models import Product, Service

class Sale(models.Model):
    sales_id = models.BigAutoField(primary_key=True)
    cust = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True)
    sales_date = models.DateField()
    sales_total_amt = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)
    sales_payment_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'sale'


class SaleItem(models.Model):
    sales_item_id = models.BigAutoField(primary_key=True)
    sales = models.ForeignKey(Sale, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, blank=True, null=True)
    prod = models.ForeignKey(Product, on_delete=models.PROTECT, blank=True, null=True)
    sale_item_type = models.CharField(max_length=50, blank=True, null=True)
    sales_item_qty = models.IntegerField(blank=True, null=True)
    sales_item_price = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)

    class Meta:
        db_table = 'sale_item'
