from django.db.models import *
from django.core.validators import RegexValidator
from pos.models import SaleItem
from hrm.models import Employee
from decimal import Decimal
class Commission(Model):
    com_id = BigAutoField(primary_key=True)
    sales_item = ForeignKey(SaleItem, on_delete=PROTECT)
    emp = ForeignKey(Employee, on_delete=PROTECT)
    com_amt = DecimalField(max_digits=1000, decimal_places=10)
    com_datetime = DateTimeField(blank=True, null=True)
    com_type = CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'commission'

class CommissionSharingPlan(Model):
    com_sharing_id = BigAutoField(primary_key=True)
    com_sharing_name = CharField(max_length=150, blank=False, null= False)
    com_sharing_desc = TextField(max_length=350, blank=True, null=True)
    class Meta:
        db_table = 'commission_sharing_plan'
        unique_together = (('com_sharing_name',))

class CommissionSharingDetail(Model):
    com_sharing_detail_id = BigAutoField(primary_key=True)
    sales = ForeignKey('pos.Sale', on_delete=PROTECT, related_name='commissionsharingdetail', null=True, blank=True)
    sales_item = ForeignKey('pos.SaleItem', on_delete=PROTECT, related_name='commissionsharingdetail', null=True, blank=True)
    com_sharing = ForeignKey(CommissionSharingPlan, on_delete=PROTECT, related_name='commissionsharingplan', null=False, blank=False)
    emp_share_percent = ManyToManyField('hrm.Employee', related_name='commissionsharingdetail', through='EmployeeCommissionSharingPercentage')

    class Meta:
        db_table = 'commission_sharing_detail'

class EmployeeCommissionSharingPercentage(Model):
    com_sharing_detail = ForeignKey(CommissionSharingDetail, related_name='employeecommissionsharingpercentage', on_delete=PROTECT)
    emp = ForeignKey('hrm.Employee', related_name='employeecommissionsharingpercentage', on_delete=PROTECT)
    share_percent = DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if self.percentage_share == 0.0:
            # Set default equal percentage among all involved employees
            employees_count = self.commission_sharing.employees.count()
            self.percentage_share = Decimal('1.0') / employees_count
        super().save(*args, **kwargs)
    class Meta:
        db_table = 'employee_commission_sharing_percentage'

class ProductCommissionStructure(Model):
    prod_com_id = BigAutoField(primary_key=True)
    prod_com_type = CharField(max_length=50, blank=True, null=True, unique=True)
    prod_com_rate = DecimalField(max_digits=1000, decimal_places=10)

    class Meta:
        db_table = 'product_commission_structure'

class ServiceCommissionStructure(Model):
    service_com_id = BigAutoField(primary_key=True)
    service_com_type = CharField(max_length=50, blank=True, null=True, unique=True) #refers to sales/doing treatment
    service_com_category = CharField(max_length=50, blank=True, null=True, unique=True) #refers to the category of commission
    service_com_rate = DecimalField(max_digits=1000, decimal_places=10)
    
    class Meta:
        db_table = 'service_commission_structure'
        
class PercentageMultiplierThreshold(Model):
    thres_id = BigAutoField(primary_key=True)
    sales_amt = DecimalField(max_digits=1000, decimal_places=10) #sales threshold level
    percent_multiplier = DecimalField(max_digits=3, decimal_places=2) #respective multiplier for each threshold level

    class Meta:
        db_table = 'percentage_multiplier_threshold'

class BankDatabase(Model):
    bank_name = CharField(max_length=100)
    bank_swift_code = CharField(max_length=11, validators=[
        RegexValidator(r'^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$', message='Invalid SWIFT code')
    ])
    bank_city = CharField(max_length=100, validators=[
        RegexValidator(r'^[A-Za-z\s]+$', message='City name can only contain letters and spaces')
    ])

    class Meta:
        db_table = 'bank_database'