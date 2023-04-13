from django.urls import path, include
from inventory.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('product', ProductViewSet)
router.register('service', ServiceViewSet)

app_name = 'inventory'


urlpatterns = [
    path('', include(router.urls)),
]