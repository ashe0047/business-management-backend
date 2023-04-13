from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from auth_core.models import User
from core.models import *
from crm.models import *
from hrm.models import *
from inventory.models import *
from pos.models import *
from enum import Enum

class Roles(Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"
    MANAGER = "manager"


def init_roles_and_permissions():
    manager_role = Group.objects.create(name=Roles.MANAGER.value)
    employee_role = Group.objects.create(name=Roles.EMPLOYEE.value)

    
