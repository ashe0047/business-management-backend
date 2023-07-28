'''
    Business logic of sale and saleitem data is implemented here through serializer Validators
'''

from typing import Any, Union
from datetime import datetime
from collections import OrderedDict
from pos.models.models import Sale, SaleItem
from marketing.models.models import *
from rest_framework.serializers import ValidationError

class SaleValidator:
    '''
    '''
    def __init__(self) -> None:
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass


class SaleItemValidator:
    '''
    Validator class for checking:
        1. Only one and at least one of inventory fields must have a value
    '''
    #class variables
    requires_context = False
    inventory_fields = ['service', 'pkg_sub', 'prod', 'voucher_sale']

    def __init__(self) -> None:
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass

    @staticmethod
    def get_inventory_field(value: OrderedDict):
        for field in __class__.inventory_fields:
            if field in value and value[field] is not None:
                return {'instance': value[field], 'field_name': field}
            
    def validate_inventory_fields(self, value:OrderedDict):
        '''
        '''
        count = 0
        for field in __class__.inventory_fields:
            if field in value and value[field] is not None:
                count += 1 

        # Ensure that exactly one field and at least one field has a value
        if count == 0:
            raise ValidationError("At least one field is required.")
        elif count > 1:
            raise ValidationError("Exactly one field is required.")
        
class VoucherUseValidator:
    '''
    Validator class for checking:
        SaleItem:
            1. Voucher usage on discounted item
            2. Type of voucher used that is allowed
            3. Voucher redemption limit
        Sale:
            1. Voucher use in both sale and saleitem
            2. Presence of saleitem if voucher is used
            3. Voucher usage on discounted item
            4. Type of voucher used that is allowed
            5. Voucher redemption limit    
    '''
    requires_context = True

    def __init__(self) -> None:
        pass

    def __call__(self, value: OrderedDict, serializer) :
        from pos.serializers.sale_serializers import BaseSaleItemSerializer, SaleSerializer #delayed import to avoid circular dependency error

        if isinstance(serializer, SaleSerializer):
            #check if voucher is used
            if value.get('gen_voucher_use', None):
                if value.get('saleitem', None):
                    self.gen_voucher_use_constraint(value)
                else:
                    raise ValidationError('saleitems must exist in order to use vouchers')
        elif isinstance(serializer, BaseSaleItemSerializer):
            #if both voucher is used in both sale and saleitem
            if value.get('voucher_use', None) and serializer.context.get('gen_voucher_use', None):
                    raise ValidationError('Voucher cannot be used on saleitem if Generic Voucher is used')
            #if voucher is used in saleitem but not sale
            elif value.get('voucher_use', None) and not serializer.context.get('gen_voucher_use', None):
                self.voucher_use_contraint(value)
            #if voucher is used in sale but not saleitem    
            elif not value.get('voucher_use', None) and serializer.context.get('gen_voucher_use', None):
                self.discount_constraint_check(value)

    def discount_constraint_check(self, value: OrderedDict):
        inventory_field_names = ['service', 'pkg_sub', 'prod', 'voucher']
        for field_name in inventory_field_names:
            field = value.get(field_name)
            if field:
                if field_name == inventory_field_names[1]:
                    discount_field = field.pkg.pkg_discount_percent
                    if discount_field:
                        raise ValidationError('Voucher cannot be used on items with discounts')
                else:
                    discount_field_name = field_name + '_discount_percent'
                    discount_field = getattr(field, discount_field_name)
                    if discount_field:
                        raise ValidationError('Voucher cannot be used on items with discounts')
    
    def validate_voucher_use_saleitem_type(self, value:OrderedDict):
        voucher_use = value.get('voucher_use', None)
        if voucher_use:
            if isinstance(voucher_use, CategoryVoucher):
                voucher_category = voucher_use.category
                inventory_info = SaleItemValidator.get_inventory_field(value)
                saleitem_category = getattr(inventory_info['instance'], inventory_info['field_name']+'_category')
                if voucher_category != saleitem_category:
                    raise ValidationError('Voucher used is invalid as this voucher is not meant for this '+inventory_info['field_name']+' category')
                
            elif isinstance(voucher_use, ItemVoucher):
                allowed_voucher_item_type = voucher_use.inventory_item_info['instances']
                inventory_info = SaleItemValidator.get_inventory_field(value)
                #inventory field is pkg_sub
                if inventory_info['field_name'] == SaleItemValidator.inventory_fields[1]:
                    saleitem_type = inventory_info['instance'].pkg
                else:
                    saleitem_type = inventory_info['instance']

                if saleitem_type not in allowed_voucher_item_type:
                    raise ValidationError('Voucher used is not meant for this '+inventory_info['field_name']+' item')

    def voucher_use_contraint(self, value: OrderedDict):
        # if not isinstance(saleitem.cat_item_voucher, (CategoryVoucher, ItemVoucher)):
        voucher_use_type = ContentType.objects.get_for_model(value['voucher_use'])
        if voucher_use_type.model not in SaleItem.ALLOWED_VOUCHER_USE_TYPES:
            raise ValidationError("Voucher use type is not valid")
        
        # if saleitem.cat_item_voucher.voucher_usage_limit - saleitem.cat_item_voucher.voucher_redemption_count <= 0:
        if not value['voucher_use'].voucher_redeemable:
            raise ValidationError('Voucher is invalid as it has passed its redemption limit')
        
        #check if saleitem is discounted
        self.discount_constraint_check(value)

        #check if voucher use type on inventory item is correct
        self.validate_voucher_use_saleitem_type(value)

        #Validate voucher date contraint
        self.validate_voucher_use_date(value['voucher_use'])
    
    def gen_voucher_use_constraint(self, value: OrderedDict):
        #check if voucher type used is correct
        for voucher in value['gen_voucher_use']:
            # if not isinstance(voucher, GenericVoucher):
            if not isinstance(voucher, GenericVoucher):
                raise ValidationError('Voucher type is not valid')

            if not voucher.voucher_redeemable:
                raise ValidationError('Voucher is invalid as it has passed its redemption limit')
            
            #Validate voucher date contraint
            self.validate_voucher_use_date(voucher)

        salesitem_instances = value['saleitem']
        for saleitem in salesitem_instances:
            self.discount_constraint_check(saleitem)
            
    def validate_voucher_use_date(self, voucher: Union[GenericVoucher, CategoryVoucher, ItemVoucher]):
        start_date = getattr(voucher, 'voucher_start_date', None)
        end_date = getattr(voucher, 'voucher_end_date', None)
        current_date = datetime.now().date()

        if start_date and end_date:
            if current_date < start_date or current_date > end_date:
                raise ValidationError('Voucher cannot be used as it has either expired or have not started')
        elif start_date and end_date is None:
            if current_date < start_date:
                raise ValidationError('Voucher cannot be used as it has not started')
        elif start_date is None and end_date:
            if current_date > end_date:
                raise ValidationError('Voucher cannot be used as it has expired')
            
