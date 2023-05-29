from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group
from auth_core.management.commands.roles import Roles

class DeleteSalesPerm(BasePermission):
    
    #not employee role check
    def has_permission(self, request, view):
        if request.method in ["DELETE"]:
            return not request.user.groups.filter(name=Roles.EMPLOYEE.value).exists()
        return True
    
