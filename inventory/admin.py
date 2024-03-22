from django.contrib import admin
from inventory.models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ['prod_name']+[field.name for field in Product._meta.fields if 'id' not in field.name and field.name not in ['prod_ingredients', 'prod_desc', 'prod_name']]
    
class ProductSupplierAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductSupplier._meta.fields if 'id' not in field.name]

class ServiceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Service._meta.fields if 'id' not in field.name]

class ServicePackageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ServicePackage._meta.fields if 'id' not in field.name and field.name not in ['service']]

class ServicePackageServiceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ServicePackageService._meta.fields if 'id' not in field.name]

class InventoryCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in InventoryCategory._meta.fields if 'id' not in field.name]

class ProductBrandAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductBrand._meta.fields if 'id' not in field.name]

class ProductUnitSizeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductUnitSize._meta.fields if 'id' not in field.name]

class ProductPackageSizeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductPackageSize._meta.fields if 'id' not in field.name]

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSupplier, ProductSupplierAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServicePackage, ServicePackageAdmin)
admin.site.register(ServicePackageService, ServicePackageServiceAdmin)
admin.site.register(InventoryCategory, InventoryCategoryAdmin)
admin.site.register(ProductBrand, ProductBrandAdmin)
admin.site.register(ProductUnitSize, ProductUnitSizeAdmin)
admin.site.register(ProductPackageSize, ProductPackageSizeAdmin)