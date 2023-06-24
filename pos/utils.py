from pos.models import PackageSubscription
from django.db import transaction

@transaction.atomic
def update_pkg_sub_payment(pkg_sub_id, sales_item_price):
    try:
        pkg_sub_instance = PackageSubscription.objects.get(pkg_sub_id=pkg_sub_id)
        pkg_sub_instance.paid_amt += sales_item_price
        pkg_sub_instance.save()
        return pkg_sub_instance
    except Exception as e:
        raise e