'''
    Business logic of voucher data is implemented here through serializer Validators
'''

from typing import Any, Union
from collections import OrderedDict
from marketing.models.models import *
from rest_framework.serializers import ValidationError



class VoucherValidator:
    '''
    

    '''
    requires_context = False

    def __init__(self) -> None:
        pass

    def __call__(self, value: OrderedDict) -> Any:

        self.validate_voucher_discount_fields(value)
    
    def validate_voucher_discount_fields(self, value:OrderedDict):
        '''
        Validation for assigning only one of service,product or package subscription to a single sale item instance
        '''
        voucher_use_discount_amt = value.get('voucher_use_discount_amt', None)
        voucher_use_discount_percent = value.get('voucher_use_discount_percent', None)

        if voucher_use_discount_percent and voucher_use_discount_amt:
            raise ValidationError("Only one of voucher_use_discount_percent or voucher_use_discount_amt field can have a value.")
        elif not voucher_use_discount_percent and not voucher_use_discount_amt:
            raise ValidationError("At least one of voucher_use_discount_percent or voucher_use_discount_amt field must have a value")
        
        if voucher_use_discount_percent > 1 or voucher_use_discount_percent < 0:
            raise ValidationError("voucher_use_discount_percent value must be between 0 and 1")
        
class GenericVoucherValidator(VoucherValidator):
    '''
    '''
    requires_context = False

    def __init__(self) -> None:
        pass

    def __call__(self, value:OrderedDict) -> Any:
        pass

class CategoryVoucherValidator(VoucherValidator):
    '''
    '''
    requires_context = False

    def __init__(self) -> None:
        pass

    def __call__(self, value:OrderedDict) -> Any:
        pass

class ItemVoucherValidator(VoucherValidator):
    '''
    '''
    requires_context = False

    def __init__(self) -> None:
        pass

    def __call__(self, value:OrderedDict) -> Any:
        
        self.validate_voucher_inventory_fields(value)

    def validate_voucher_inventory_fields(self, value:OrderedDict):
        service = value.get('service', None)
        pkg = value.get('pkg', None)
        prod = value.get('prod', None)

        if service and (pkg or prod):
            raise ValidationError("Only one of service,prod or pkg field can have a value.")
        
        if pkg and (service or prod):
            raise ValidationError("Only one of service,prod or pkg field can have a value.")
        
        if prod and (service or pkg):
            raise ValidationError("Only one of service,prod or pkg field can have a value.")