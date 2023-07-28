from django.urls import path, include
from crm.views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('treatment', TreatmentViewset)

app_name = 'crm'

urlpatterns = [
    path('cust/', CustomersView.as_view(), name='customer_list_view'),
    path('cust/<int:pk>/', CustomerView.as_view(), name='customer_view'),
    path('', include(router.urls)),
]