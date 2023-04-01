from django.db import models
from pos.models import SaleItem
from hrm.models import Employee

class Commission(models.Model):
    com_id = models.BigAutoField(primary_key=True)
    sales_item = models.ForeignKey(SaleItem, on_delete=models.PROTECT)
    emp = models.ForeignKey(Employee, on_delete=models.PROTECT)
    com_amt = models.DecimalField(max_digits=1000, decimal_places=10)
    com_date = models.DateField(blank=True, null=True)
    com_type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'commission'