from django.urls import path, include
from inventory.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('product', ProductViewSet)
router.register('service', ServiceViewSet)
router.register('servicepackage', ServicePackageViewSet)
router.register('inventorycategory', InventoryCategoryViewset)
app_name = 'inventory'


urlpatterns = [
    path('', include(router.urls)),
]