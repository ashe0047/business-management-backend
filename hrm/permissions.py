from rest_framework.permissions import BasePermission, DjangoModelPermissions, DjangoObjectPermissions
from auth_core.management.commands.roles import Roles

class EditEmployeeRecordPermission(BasePermission):
    
    def has_permission(self, request, view):
        #check if user trying too change salary
        if 'emp_salary' in request.data:
            #check if user is admin
            return request.user.is_staff
                     
        return True

class ViewAllEmployeeRecordPermission(BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.filter(name=Roles.EMPLOYEE.value).exists()


class CreateEmployeeRecordPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST']:
            #check if user trying to create employee record is admin as user creating the record can input salary field
            return request.user.is_staff
        
        return True