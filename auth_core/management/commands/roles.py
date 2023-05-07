from django.contrib.auth.models import Permission
from auth_core.models import Group
from django.contrib.contenttypes.models import ContentType
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
    for role in list(Roles):
        if not Group.objects.filter(name=role.value).exists():
            Group.objects.create(name=role.value)

    
