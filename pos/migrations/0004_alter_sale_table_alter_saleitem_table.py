# Generated by Django 4.1.7 on 2023-04-01 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0003_alter_sale_table_alter_saleitem_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='sale',
            table='sales',
        ),
        migrations.AlterModelTable(
            name='saleitem',
            table='sales_item',
        ),
    ]