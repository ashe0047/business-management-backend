from collections import OrderedDict
from rest_framework.serializers import ValidationError


class ProductValidator:
    '''
    Validator class for checking:
        Product:
            1. Discount field constraints
    '''
    requires_context = False

    def __init__(self) -> None:
        pass

    def __call__(self, value: OrderedDict):
        self.validate_discount_field(value)

    def validate_discount_field(self, value: OrderedDict):
        prod_discount_percent = value.get('prod_discount_percent', None)
        if prod_discount_percent:
            if prod_discount_percent > 1 or prod_discount_percent < 0:
                raise ValidationError("prod_discount_percent value must be between 0 and 1")

class ServiceValidator:
    '''
    Validator class for checking:
        Service:
            1. Discount field constraints
    '''
    requires_context = False

    def __init__(self) -> None:
        pass

    def __call__(self, value: OrderedDict):
        self.validate_discount_field(value)

    def validate_discount_field(self, value: OrderedDict):
        service_discount_percent = value.get('service_discount_percent', None)
        if service_discount_percent:
            if service_discount_percent > 1 or service_discount_percent < 0:
                raise ValidationError("service_discount_percent value must be between 0 and 1")
            
class ServicePackageValidator:
    '''
    Validator class for checking:
        ServicePackage:
            1. Discount field constraints
    '''
    requires_context = False

    def __init__(self) -> None:
        pass

    def __call__(self, value: OrderedDict):
        self.validate_discount_field(value)

    def validate_discount_field(self, value: OrderedDict):
        pkg_discount_percent = value.get('pkg_discount_percent', None)
        if pkg_discount_percent:
            if pkg_discount_percent > 1 or pkg_discount_percent < 0:
                raise ValidationError("pkg_discount_percent value must be between 0 and 1")