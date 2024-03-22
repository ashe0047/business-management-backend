from django.db.models.signals import pre_save, m2m_changed, post_delete, post_save
from django.db.models import *
from django.dispatch import receiver
from typing import Union
from pos.models.models import Sale, SaleItem, VoucherUsage

#update voucher use,user limit depending on type of voucher coming from pos
class VoucherSignalHandler:
    cleared_vouchers = None
    def __init__(self) -> None:
        pass

    @classmethod
    def update_generic_voucher_redemption_count(cls, sender, instance, action, reverse, model, pk_set, **kwargs):
        if not reverse:
            if action == 'post_add':
                voucher_instances = instance.gen_voucher_use.all()
                for voucher_instance in voucher_instances:
                        if not voucher_instance.no_usage_limit:
                            voucher_instance.voucher_redemption_count += 1
                            voucher_instance.save()
            if action == 'pre_clear':
                #store the vouchers that are going to be cleared before clearing
                cls.cleared_vouchers = list(instance.gen_voucher_use.all()).copy()
            if action == 'post_clear':
                #retrieve the stored voucher instances so that it can be updated
                for voucher_instance in cls.cleared_vouchers:
                    if not voucher_instance.no_usage_limit:
                        voucher_instance.voucher_redemption_count -= 1
                        voucher_instance.save()
    @classmethod
    def update_item_cat_voucher_redemption_count(cls, sender: SaleItem, instance: SaleItem, signal, **kwargs):
        if signal == pre_save:
            original_saleitem_instance = None

            # Check if the save operation for SaleItem is an update
            if instance.pk is not None:
                # Retrieve the original instance from the database
                original_saleitem_instance = sender.objects.get(pk=instance.pk)

                #check if there is a change in the voucher_use field
                if original_saleitem_instance is not None and original_saleitem_instance.voucher_use != instance.voucher_use:
                    original_voucher_instance = original_saleitem_instance.voucher_use
                    voucher_instance = instance.voucher_use
                    #check what kind of change occured, adding, removing or changing of voucher
                    if original_voucher_instance is not None and voucher_instance is not None:
                        original_voucher_instance.voucher_redemption_count -= 1
                        original_voucher_instance.save()
                        voucher_instance.voucher_redemption_count += 1
                        voucher_instance.save()
                    elif original_voucher_instance is not None and voucher_instance is None:
                        original_voucher_instance.voucher_redemption_count -= 1
                        original_voucher_instance.save()
                    elif original_voucher_instance is None and voucher_instance is not None:
                        voucher_instance.voucher_redemption_count += 1
                        voucher_instance.save()
            else:
                #check if voucher is added for the newly created SaleItem
                if instance.voucher_use is not None:
                    instance.voucher_use.voucher_redemption_count += 1
                    instance.voucher_use.save()
        
        elif signal == post_delete:
            if instance.voucher_use is not None:
                instance.voucher_use.voucher_redemption_count -= 1
                instance.voucher_use.save() 

# @receiver([pre_save, post_delete], sender=SaleItem)
# def update_item_cat_voucher_redemption_count(sender: SaleItem, instance: SaleItem, signal, **kwargs):
#     #Update redemption count when SaleItem is created or deleted
#     if instance.pk is not None:

#     instance.voucher_use.voucher_redemption_count = len(instance.voucher_use.saleitem_use.all())
#     instance.voucher_use.save()
#might need to update user limit as well
                
#Signal class init
voucher_signal_handler = VoucherSignalHandler()
m2m_changed.connect(voucher_signal_handler.update_generic_voucher_redemption_count, sender=Sale.gen_voucher_use.through)
pre_save.connect(voucher_signal_handler.update_item_cat_voucher_redemption_count, sender=SaleItem)
post_save.connect(voucher_signal_handler.update_item_cat_voucher_redemption_count, sender=SaleItem)