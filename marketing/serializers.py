from rest_framework import serializers
from marketing.models import *
from core.utils import context_update_parent

class BaseGenericVoucher(serializers.ModelSerializer):
    pass

