from django.contrib.auth.models import Permission
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
   
