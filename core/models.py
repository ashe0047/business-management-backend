from typing import Iterable, Optional
from django.db.models import *
from django.core.exceptions import ValidationError
from hrm.models import Employee


class CommissionSummary(Model):
    pass

#By Employee and Month, aggregate summary table of variable commission from commission sharing detail
#Updated by signals
class VariableCommissionSummary(Model):
    var_com_id = BigAutoField(primary_key=True)
    emp = ForeignKey(Employee, on_delete=PROTECT)
    date = DateField()
    gross_sales = DecimalField(max_digits=1000, decimal_places=2, default=0)
    thres = ForeignKey("core.PercentageMultiplierThreshold", on_delete=PROTECT, related_name='commissionsummary', null=True, blank=True)
    adjusted_sales = DecimalField(max_digits=1000, decimal_places=2, default=0)
    com_amt = DecimalField(max_digits=1000, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        #set day for all entries to a constant so that the entries can be aggregated using month and year only
        self.date = self.date.replace(day=1)
        return super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'variable_commission_summary'
        verbose_name_plural = "Variable Commission Summaries"
        unique_together = (('emp', 'date',),)


    
    # def save(self, *args, **kwargs):
    #     thres_levels = PercentageMultiplierThreshold.objects.all()
    #     for thres in thres_levels:
    #         if self.gross_sales < thres.sales_amt:
    #             self.thres = thres
    #     self.adjusted_sales = self.thres.percent_multiplier * self.gross_sales
    #     return super().save(*args, **kwargs)
    
#updated internally by signals
class FixedCommissionSummary(Model):
    fixed_com_id = BigAutoField(primary_key=True)
    emp = ForeignKey(Employee, on_delete=PROTECT)
    date = DateField()
    com_amt = DecimalField(max_digits=1000, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        #set day for all entries to a constant so that the entries can be aggregated using month and year only
        self.date = self.date.replace(day=1)
        return super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'fixed_commission_summary'
        verbose_name_plural = 'Fixed Commission Summaries'
        unique_together = (('emp', 'date',),)

    

#junction table for saleitem and employee to track portion of share fixed comm using percentage from employeecommission
# class FixedCommissionSharing(Model):
#     com_id = BigAutoField(primary_key=True)
#     sales_item = ForeignKey("pos.SaleItem", on_delete=PROTECT, null=False, blank=False, related_name='fixedcommissionsharing')
#     com_amt = DecimalField(max_digits=1000, decimal_places=10)
#     com_datetime = DateTimeField(auto_now_add=True, blank=True, null=True)
#     # service_com = ForeignKey("core.ServiceCommissionStructure", on_delete=PROTECT, null=True, blank=True, related_name='fixedcommissionsharing')
#     # voucher_com = ForeignKey("core.VoucherCommissionStructure", on_delete=PROTECT, null=True, blank=True, related_name='fixedcommissionsharing')
#     emp_share_percent = ManyToManyField('hrm.Employee', related_name='fixedcommissionsharing', through='EmployeeFixedCommissionSharing')
    
#     class Meta:
#         db_table = 'fixed_commission_sharing'

# class EmployeeFixedCommissionSharing(Model):
#     com = ForeignKey(FixedCommissionSharing, related_name='employeefixedcommissionsharing', on_delete=PROTECT)
#     emp = ForeignKey(Employee, related_name='employeefixedcommissionsharing', on_delete=PROTECT)
#     share_percent = DecimalField(max_digits=3, decimal_places=2)
#     share_amount = DecimalField(max_digits=1000, decimal_places=10)

#     class Meta:
#         db_table = 'employee_fixed_commission_sharing'
        
#sales target distribution among employees for each sale/sale item
class Commission(Model):
    com_id = BigAutoField(primary_key=True)
    sales = OneToOneField('pos.Sale', on_delete=PROTECT, related_name='commission', null=True, blank=True) #null if salesitem sharing
    sales_item = OneToOneField('pos.SaleItem', on_delete=PROTECT, related_name='commission', null=True, blank=True) #null if sales sharing
    datetime = DateTimeField(auto_now_add=True, null=False, blank=False)
    # com_sharing = ForeignKey(CommissionSharingPlan, on_delete=PROTECT, related_name='commissionsharingplan', null=False, blank=False)
    custom_sharing = BooleanField(default=False)
    emp_share_percent = ManyToManyField('hrm.Employee', related_name='commission', through='EmployeeCommission') #percentage for each emp involved

    def clean(self):
        if self.sales and self.sales_item:
            raise ValidationError("Only one of sales or sales_item field can have a value.")
        elif not self.sales and not self.sales_item:
            raise ValidationError("At least one of sales or sales_item field must have a value")
        super().clean()

    class Meta:
        db_table = 'commission'
        unique_together = (('sales',),('sales_item',),)

#Junction table to link commissionsharing table to employee while tracking sharing percentage 
class EmployeeCommission(Model):
    com = ForeignKey(Commission, related_name='employeecommission', on_delete=PROTECT)
    emp = ForeignKey(Employee, related_name='employeecommission', on_delete=PROTECT)
    share_percent = DecimalField(max_digits=3, decimal_places=2)
    sales_amount = DecimalField(max_digits=1000, decimal_places=10)
    fixed_com_amount = DecimalField(max_digits=1000, decimal_places=10)
    

    # def save(self, *args, **kwargs):
    #     if not self.com_sharing_detail.custom_percent:
    #         # Set default equal percentage among all involved employees
    #         employees_count = self.com_sharing_detail.emp_share_percent.count()
    #         self.share_percent = Decimal('1.0') / employees_count
    #     super().save(*args, **kwargs)

    class Meta:
        db_table = 'employee_commission'
        unique_together = (('com','emp',),)

class ProductCommissionStructure(Model):
    prod_com_id = BigAutoField(primary_key=True)
    prod_com_type = CharField(max_length=50, blank=True, null=True, unique=True)
    prod_com_rate = DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)
    prod_com_amt = DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)

    class Meta:
        db_table = 'product_commission_structure'

class ServiceCommissionStructure(Model):
    service_com_id = BigAutoField(primary_key=True)
    service_com_type = CharField(max_length=50, blank=True, null=True, unique=True) #refers to sales/doing treatment
    service_com_category = CharField(max_length=50, blank=True, null=True, unique=True) #refers to the category of commission
    service_com_rate = DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    service_com_amt = DecimalField(max_digits=1000, decimal_places=10, null=True, blank=True)
    
    def clean(self):
        if self.service_com_rate and self.service_com_amt:
            raise ValidationError("Only one of service_com_rate or service_com_amt field can have a value.")
        elif not self.service_com_rate and not self.service_com_amt:
            raise ValidationError("At least one of service_com_rate or service_com_amt field must have a value")
        
        if self.service_com_rate > 1 or self.service_com_rate <0:
            raise ValidationError('service_com_rate value must be between 0 and 1')
        super().clean()

    class Meta:
        db_table = 'service_commission_structure'

class VoucherCommissionStructure(Model):
    voucher_com_id = BigAutoField(primary_key=True)
    voucher_com_type = CharField(max_length=50, blank=True, null=True, unique=True) 
    voucher_com_rate = DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)
    voucher_com_amt = DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)
    
    def clean(self):
        if self.voucher_com_rate and self.voucher_com_amt:
            raise ValidationError("Only one of voucher_com_rate or voucher_com_amt field can have a value.")
        elif not self.voucher_com_rate and not self.voucher_com_amt:
            raise ValidationError("At least one of voucher_com_rate or voucher_com_amt field must have a value")
        
        if self.voucher_com_rate > 1 or self.voucher_com_rate <0:
            raise ValidationError('voucher_com_rate value must be between 0 and 1')

    class Meta:
        db_table = 'voucher_commission_structure'
        
class PercentageMultiplierThreshold(Model):
    thres_id = BigAutoField(primary_key=True)
    sales_amt = DecimalField(max_digits=1000, decimal_places=10) #sales threshold level
    percent_multiplier = DecimalField(max_digits=3, decimal_places=2) #respective multiplier for each threshold level
    bonus_amt = DecimalField(max_digits=1000, decimal_places=10, null=True, blank=True) #bonus commission that might be given for higher threshold levels

    class Meta:
        db_table = 'percentage_multiplier_threshold'
        unique_together = (('sales_amt','percent_multiplier',),)

