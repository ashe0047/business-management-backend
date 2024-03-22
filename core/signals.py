from django.db.models.signals import post_save, m2m_changed
from django.db.models import *
from django.dispatch import receiver
from core.models import *

@receiver(m2m_changed, sender=Commission.emp_share_percent.through)
def variable_commission_update(sender, instance: Commission, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add' and not reverse:
        #aggregate factors
        emp_instances = instance.emp_share_percent.all()
        month = instance.datetime.month
        year = instance.datetime.year

        #Aggregate operations
        for emp in emp_instances:
            #Retrieve only the records from the latest month and year
            employeecommission_monthyear_set = EmployeeCommission.objects.filter(emp=emp, com__datetime__month=month, com__datetime__year=year)
            gross_sales = employeecommission_monthyear_set.aggregate(total=Sum('sales_amount'))['total'] or 0
            # min_sales_amt = PercentageMultiplierThreshold.objects.order_by('sales_amt').first().sales_amt
            # thres = next((thres_level for thres_level in PercentageMultiplierThreshold.objects.all() if gross_sales < thres_level.sales_amt and gross_sales > min_sales_amt), None)
            
            #Retrieve all threshold levels that is lower than the sales_amt then order by descending order to get the highest threshold level that is exceeded by the sales_amt
            thres = PercentageMultiplierThreshold.objects.filter(sales_amt__lte=gross_sales).order_by('-sales_amt').first()
            
            #Further filter employeesalessharing to exclude service and voucher items which gives fixedcommission
            employeecommission_exclservicevoucher_set = employeecommission_monthyear_set.filter(com__sales_item__service=None, com__sales_item__voucher=None)
            adjusted_sales = employeecommission_exclservicevoucher_set.aggregate(total=Sum('sales_amount'))['total'] or 0
            
            #total commission amount
            com_amt = 0
            if thres:
                com_amt += thres.percent_multiplier * adjusted_sales 
                if thres.bonus_amt:
                    com_amt += thres.bonus_amt

            defaults = {
                'gross_sales': gross_sales,
                'thres': thres,
                'adjusted_sales': adjusted_sales,
                'com_amt': com_amt
            }

            #update related variable commission summary instance
            VariableCommissionSummary.objects.update_or_create(emp=emp, date=instance.datetime.date().replace(day=1), defaults=defaults)

@receiver(m2m_changed, sender=Commission.emp_share_percent.through)
def fixed_commission_update(sender, instance: Commission, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add' and not reverse:
        #aggregate factors
        emp_instances = instance.emp_share_percent.all()
        month = instance.datetime.month
        year = instance.datetime.year
        # print(month)
        #Aggregate operations
        for emp in emp_instances:
            #Retrieve only the records from the latest month and year
            employeecommission_monthyear_set = EmployeeCommission.objects.filter(emp=emp, com__datetime__month=month, com__datetime__year=year)
            fixed_com_amount = employeecommission_monthyear_set.aggregate(total=Sum('fixed_com_amount'))['total']or 0

            #updated related variable commission summary instance
            FixedCommissionSummary.objects.update_or_create(emp=emp, date=instance.datetime.date().replace(day=1), defaults={'com_amt': fixed_com_amount})
