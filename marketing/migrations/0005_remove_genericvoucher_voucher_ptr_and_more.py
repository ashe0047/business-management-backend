# Generated by Django 4.2 on 2023-06-26 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0004_remove_voucher_voucher_discount_value_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genericvoucher',
            name='voucher_ptr',
        ),
        migrations.RemoveField(
            model_name='itemvoucher',
            name='pkg',
        ),
        migrations.RemoveField(
            model_name='itemvoucher',
            name='prod',
        ),
        migrations.RemoveField(
            model_name='itemvoucher',
            name='service',
        ),
        migrations.RemoveField(
            model_name='itemvoucher',
            name='voucher_ptr',
        ),
        migrations.DeleteModel(
            name='CategoryVoucher',
        ),
        migrations.DeleteModel(
            name='GenericVoucher',
        ),
        migrations.DeleteModel(
            name='ItemVoucher',
        ),
    ]
