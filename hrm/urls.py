from django.urls import path, include
from hrm.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('bankdatabase', BankDatabaseViewset)
    
urlpatterns = [
    path('emp/', EmployeeView.as_view(), name='employee_view'),
    path('emps/', EmployeesView.as_view(), name='get_employee_list'),
    # path('remove/<int:pk>', DeleteUserView.as_view(), name='user_remove'),
    path('emp/accounts/', GetEmployeeViewWithAccounts.as_view(), name='get_employee_details_with_accounts'),
    path('', include(router.urls))
]
