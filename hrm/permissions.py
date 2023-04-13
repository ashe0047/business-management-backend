from rest_framework.permissions import BasePermission, DjangoModelPermissions, DjangoObjectPermissions
from auth_core.management.commands.roles import Roles

class EditEmployeeRecordPermission(BasePermission):
    
    def has_permission(self, request, view):
        #check if user trying too change salary
        if 'emp_salary' in request.data:
            #check if user is admin
            if request.user.is_staff:
                return True
            return False   
                     
        return True

class ViewAllEmployeeRecordPermission(BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.filter(name=Roles.EMPLOYEE.value).exists()

