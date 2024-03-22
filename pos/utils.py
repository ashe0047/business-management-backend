from marketing.models.models import *
from django.apps import apps
from django.db import transaction
from django.core.exceptions import ValidationError

@transaction.atomic
def update_pkg_sub_payment(pkg_sub_id, serializer, paid_amt):
    try:
        pkg_sub_instance = serializer.fields['pkg_sub'].Meta.model.objects.get(pkg_sub_id=pkg_sub_id)
        pkg_sub_instance.paid_amt += paid_amt
        pkg_sub_instance.save()
        return pkg_sub_instance
    except Exception as e:
        raise e

def voucher_discount_amount(voucher_info, inventory_price):
    if voucher_info is not None:
        if voucher_info['discount_type'] == 'percentage':
            return voucher_info['discount_percent'] * inventory_price
        else:
            return voucher_info['discount_amt']
    return 0
# def voucher_constraint_check(instance):
#     saleitem_class = apps.get_model('pos', 'SaleItem')
#     sale_class = apps.get_model('pos', 'Sale')
#     def discount_constraint_check(instance):
#         inventory_field_names = ['service', 'pkg_sub', 'prod', 'voucher']
#         for field_name in inventory_field_names:
#             field = getattr(instance, field_name)
#             if field:
#                 if field_name == inventory_field_names[1]:
#                     discount_field = field.pkg.pkg_discount_percent
#                     if discount_field:
#                         raise ValidationError('Voucher cannot be used on items with discounts')
#                 else:
#                     discount_field_name = field_name + '_discount_percent'
#                     discount_field = getattr(field, discount_field_name)
#                     if discount_field:
#                         raise ValidationError('Voucher cannot be used on items with discounts')
    
#     def voucher_use_contraint(saleitem: saleitem_class):
#         # if not isinstance(saleitem.cat_item_voucher, (CategoryVoucher, ItemVoucher)):
#         if saleitem.voucher_use_type.model not in saleitem.ALLOWED_VOUCHER_USE_TYPES:
#             raise ValidationError("Voucher use type is not valid")
        
#         # if saleitem.cat_item_voucher.voucher_usage_limit - saleitem.cat_item_voucher.voucher_redemption_count <= 0:
#         if not saleitem.voucher_use.voucher_redeemable:
#             raise ValidationError('Voucher is invalid as it has passed its redemption limit')
        
#         #check if saleitem is discounted
#         discount_constraint_check(saleitem)
    
#     def voucher_sale_constraint(saleitem: saleitem_class):
#         if saleitem.voucher_sale_type.model not in saleitem.ALLOWED_VOUCHER_SALE_TYPES:
#             raise ValidationError('Voucher sale type is not valid')
        
#     def gen_voucher_use_constraint(sale: sale_class):
#         #check if voucher type used is correct
#         for voucher in sale.gen_voucher_use.all():
#             # if not isinstance(voucher, GenericVoucher):
#             if not isinstance(voucher, GenericVoucher):
#                 raise ValidationError('Voucher type is not valid')

#             if not voucher.voucher_redeemable:
#                 raise ValidationError('Voucher is invalid as it has passed its redemption limit')

#         salesitem_instances = sale.saleitem.all()
#         for saleitem in salesitem_instances:
#             discount_constraint_check(saleitem)
            
#     if isinstance(instance, sale_class):
#         gen_voucher_use_constraint(instance)
#     elif isinstance(instance, saleitem_class):
#         voucher_use_contraint(instance)
#         voucher_sale_constraint(instance)


                
