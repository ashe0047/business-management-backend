from django.contrib import admin
from inventory.models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductSupplier)
admin.site.register(Service)