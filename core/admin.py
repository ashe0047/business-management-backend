from django.contrib import admin
from core.models import *

# Register your models here.
admin.site.register(ProductCommissionStructure)
admin.site.register(ServiceCommissionStructure)
admin.site.register(VoucherCommissionStructure)
admin.site.register(PercentageMultiplierThreshold)
admin.site.register(Commission)
admin.site.register(EmployeeCommission)
admin.site.register(VariableCommissionSummary)
admin.site.register(FixedCommissionSummary)