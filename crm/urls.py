from django.urls import path, include
from crm.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('customer', CustomerViewSet)

app_name = 'crm'


urlpatterns = [
    path('', include(router.urls)),
]