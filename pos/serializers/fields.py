from rest_framework.fields import Field, HiddenField, empty
from collections import OrderedDict
from marketing.models.models import *
from marketing.serializers.serializers import *
from core.common.fields import GenericForeignKeyRelatedField
from drf_spectacular.utils import extend_schema_field


    
@extend_schema_field(
    field = {'type': 'object',
                'properties': {
                    'voucher_sale_type': {
                        'type': 'string',
                    },
                    'voucher_sale_id': {
                        'type': 'integer',
                    },
                },},
    component_name = 'VoucherSaleField'
)
class VoucherSaleField(GenericForeignKeyRelatedField):
    '''
    A custom field used for Voucher object generic relationship
    '''
    def __init__(self, **kwargs):
        kwargs['content_type_field'] = 'voucher_use_type'
        kwargs['object_id_field'] = 'voucher_use_id'
        kwargs['app_label'] = 'marketing'
        super().__init__(**kwargs)
    


@extend_schema_field(
    field = {'type': 'object',
                'properties': {
                    'voucher_use_type': {
                        'type': 'string',
                    },
                    'voucher_use_id': {
                        'type': 'integer',
                    },
                },},
    component_name = 'VoucherUseField'
)
class VoucherUseField(GenericForeignKeyRelatedField):
    '''
    A custom field used for Voucher object generic relationship
    '''
    def __init__(self, **kwargs):
        kwargs['content_type_field'] = 'voucher_use_type'
        kwargs['object_id_field'] = 'voucher_use_id'
        kwargs['app_label'] = 'marketing'
        super().__init__(**kwargs)

@extend_schema_field(
    field = {'type': 'object',
                'properties': {
                    'gross': {
                        'type': 'number',
                        'format': 'double'
                    },
                    'net': {
                        'type': 'number',
                        'format': 'double'
                    },
                },},
    component_name = 'SaleItemUnitPriceField'
)   
class SaleItemUnitPriceField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        return super().to_internal_value(data)
    
    def to_representation(self, obj: SaleItem):
        return {
            'gross': obj.gross_sales_item_unit_price,
            'net': obj.net_sales_item_unit_price
        }
    
@extend_schema_field(
    field = {'type': 'object',
                'properties': {
                    'gross': {
                        'type': 'number',
                        'format': 'double'
                    },
                    'net': {
                        'type': 'number',
                        'format': 'double'
                    },
                },},
    component_name = 'SaleItemTotalPriceField'
)   
class SaleItemTotalPriceField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        return super().to_internal_value(data)
    
    def get_value(self, dictionary):
        print(dictionary)
        value = super().get_value(dictionary)
        print(value)
        return value

    def to_representation(self, obj: SaleItem):
        return {
            'gross': obj.gross_sales_item_total_price,
            'net': obj.net_sales_item_total_price
        }

@extend_schema_field(
    field = {'type': 'object',
                'properties': {
                    'gross': {
                        'type': 'number',
                        'format': 'double'
                    },
                    'net': {
                        'type': 'number',
                        'format': 'double'
                    },
                },},
    component_name = 'SalesAmountField'
)
class SalesAmountField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def to_internal_value(self, data):
        return super().to_internal_value(data)
    
    def to_representation(self, obj: Sale):
        return {
            'gross': obj.gross_sales_amt,
            'net': obj.net_sales_amt
        }