# Generated by Django 4.2 on 2023-07-10 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0013_rename_sales_payment_type_sale_sales_payment_method'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='gen_voucher_used',
            new_name='gen_voucher_use',
        ),
    ]
