from decimal import Decimal
from pos.models import Sale, PackageSubscription, SaleItem

#helper function

#context update function
def context_update_parent(current):
        #pass parent serializer to child serializer for checking
        context = current.context.copy()
        if not context.get('parent'):
            context['parent'] = current
        else:
            context['parent2'] = current
        return context

#Employee_commission percentage
def share_size_calculation(validated_data: dict):
    
    try:
        #helper functions for share size calc
        def get_sale_item_fixed_com(sale_item_instance:SaleItem):
            def increment_total_com_amt():
                com_value_field_names = [com_field_name+'_rate', com_field_name+'_amt']
                for com_value_field_name in com_value_field_names:
                        com_value_field = getattr(com_field, com_value_field_name)
                        if com_value_field:
                            #check if field is rate or actual amount
                            if com_value_field_name == com_value_field_names[0]:
                                return (com_value_field*sale_item_instance.sale_item_price)
                            elif com_value_field_name == com_value_field_names[1]:
                                return com_value_field
                raise Exception("Neither com_rate or com_amt has a value")

            inventory_fields = ['service', 'voucher', 'prod', 'pkg_sub']
            inventory_field, inventory_field_name = next((getattr(sale_item_instance, field), field) for field in inventory_fields if getattr(sale_item_instance, field) is not None)
            if isinstance(inventory_field, PackageSubscription):
                if inventory_field.fully_paid:
                    services = inventory_field.service.all()
                    services_total_com = 0
                    for service in services:
                        com_field_name = 'service_com'
                        com_field = getattr(service, com_field_name)
                        services_total_com += increment_total_com_amt()
                    return services_total_com  

            else:
                com_field_name = inventory_field_name + '_com'
                com_field = getattr(inventory_field, com_field_name)
                return increment_total_com_amt()

        def get_sales_total_fixed_com(sales_instance: Sale):
        
            sales_items = sales_instance.saleitem.all()
            total_com_amt = 0
            for sales_item in sales_items:
                total_com_amt += get_sale_item_fixed_com(sales_item)
                
            return total_com_amt
        
        for com_item in validated_data:
            #check sharing granularity
            sales = com_item['sales'] if 'sales' in com_item else None
            sales_total_fixed_com = get_sales_total_fixed_com(sales) if sales else None
            sales_item = com_item['sales_item'] if 'sales_item' in com_item else None
            #get sharing details
            emp_share_percent = com_item['emp_share_percent']
            #check if custom sharing
            custom_sharing = com_item['custom_sharing'] if 'custom_sharing' in com_item else None
            if custom_sharing:
                #loop through each detail and calc share percentage, sales amount and fixed com amount
                for item in emp_share_percent:
                    sales_amount = com_item['sales_amount'] if 'sales_amount' in item else None
                    item['share_percent'] = sales_amount/sales.sales_total_amt if sales else sales_amount/sales_item.sales_item_price
                    item['fixed_com_amount'] = item['share_percent'] * sales_total_fixed_com if sales else item['share_percent'] * get_sale_item_fixed_com(sales_item)
            else:
                for item in emp_share_percent:
                    item['share_percent'] = Decimal('1.0')/len(emp_share_percent)
                    item['sales_amount'] = sales.sales_total_amt/len(emp_share_percent) if sales else sales_item.sales_item_price/len(emp_share_percent)
                    item['fixed_com_amount'] = item['share_percent'] * sales_total_fixed_com if sales else item['share_percent'] * get_sale_item_fixed_com(sales_item)

    except Exception as e:
        raise e
