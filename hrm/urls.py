from django.urls import path, include
from hrm.views import *

    
urlpatterns = [
    path('emp', EmployeeView.as_view(), name='create_employee'),
    path('emp/all', GetEmployeeView.as_view(), name='get_employee_list'),
    # path('remove/<int:pk>', DeleteUserView.as_view(), name='user_remove'),
    path('emp/accounts', GetEmployeeViewWithAccounts.as_view(), name='get_employee_details_with_accounts'),
]