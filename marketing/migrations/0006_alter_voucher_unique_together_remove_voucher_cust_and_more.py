# Generated by Django 4.2 on 2023-06-26 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0005_remove_genericvoucher_voucher_ptr_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='voucher',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='voucher',
            name='cust',
        ),
        migrations.RemoveField(
            model_name='voucher',
            name='voucher_com',
        ),
    ]
