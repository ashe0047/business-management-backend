from django.urls import path, include
from crm.views import *


urlpatterns = [
    path('cust', CustomersView.as_view(), name='customer_list_view'),
    path('cust/<int:pk>', CustomerView.as_view(), name='customer_view'),
]