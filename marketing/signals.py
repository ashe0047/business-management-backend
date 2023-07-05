from django.db.models.signals import pre_save, m2m_changed, post_delete, post_save
from django.db.models import *
from django.dispatch import receiver
from typing import Union
from pos.models.models import Sale, SaleItem, VoucherUsage

#update voucher use,user limit depending on type of voucher coming from pos
@receiver(m2m_changed, sender=Sale.gen_voucher_used.through)
def update_generic_voucher_redemption_count(sender, instance: Union[VoucherUsage, SaleItem], action, reverse, model, pk_set, **kwargs):
    if not reverse:
        voucher_instance = instance.voucher
        if action == 'post_add':
            if voucher_instance.voucher_usage_limit:
                voucher_instance.voucher_redemption_count += 1
                voucher_instance.save()
        if action == 'post_remove':
            if voucher_instance.voucher_usage_limit:
                voucher_instance.voucher_redemption_count -= 1
                voucher_instance.save()

@receiver([pre_save, post_delete], sender=SaleItem)
def update_item_cat_voucher_redemption_count(sender: SaleItem, instance: SaleItem, signal, **kwargs):
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
                