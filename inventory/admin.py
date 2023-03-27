from django.contrib import admin
from inventory.models import *

# Register your models here.
admin.site.register(Products)
admin.site.register(ProductsSupplier)
admin.site.register(Services)