#num treatment deduction from treatment entry
from django.db.models.signals import post_save, post_delete
from django.db.models import *
from django.dispatch import receiver
from typing import Union
from crm.models.models import Treatment
from pos.models.models import PackageSubscription, PackageSubscriptionService

#update treatment left when a treatment record is entered
@receiver([post_save, post_delete], sender=Treatment)
def update_pkg_sub_treatment_left(signal, sender, instance:Treatment, **kwargs):
    pkg_sub_instance = instance.pkg_sub
    service_instance = instance.service
    pkg_sub_service_instance = PackageSubscriptionService.objects.get(service=service_instance, pkg_sub=pkg_sub_instance)
    if signal == post_save:
        created = kwargs.get('created', None) 
        if created == True:
                pkg_sub_service_instance.treatment_left -= 1
                
            
    elif signal == post_delete:
        pkg_sub_service_instance.treatment_left += 1
        
    pkg_sub_service_instance.save()