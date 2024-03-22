from django.urls import path
from pos.views import *


urlpatterns = [
    path('sale/', SalesView.as_view(), name='sale_list_view'),
    path('sale/<int:pk>/', SaleView.as_view(), name='sale_view'),
    path('saleitem/', SaleItemsView.as_view(), name='sale_item_list_view'),
    path('saleitem/<int:pk>/', SaleItemView.as_view(), name='sale_item_view'),
]