from django.contrib import admin
from core.models import *

# Register your models here.
admin.site.register(Commission)
admin.site.register(ProductCommissionStructure)
admin.site.register(ServiceCommissionStructure)
admin.site.register(PercentageMultiplierThreshold)
admin.site.register(CommissionSharingDetail)
# admin.site.register(CommissionSharingPlan)
admin.site.register(EmployeeCommissionSharingPercentage)
admin.site.register(BankDatabase)
