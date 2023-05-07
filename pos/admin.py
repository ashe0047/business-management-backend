from django.contrib import admin
from pos.models import *

# Register your models here.
admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(PackageSubscription)
admin.site.register(PackageSubscriptionService)