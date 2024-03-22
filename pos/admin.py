from django.contrib import admin
from pos.models.models import *

# Register your models here.
admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(VoucherUsage)
admin.site.register(PackageSubscription)
admin.site.register(PackageSubscriptionService)