# Generated by Django 4.2 on 2023-06-24 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_alter_inventorycategory_cat_type_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventorycategory',
            options={'verbose_name_plural': 'Inventory Categories'},
        ),
        migrations.AlterUniqueTogether(
            name='inventorycategory',
            unique_together={('cat_name',)},
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('prod_name',), ('prod_barcode',), ('prod_sku',)},
        ),
        migrations.AlterUniqueTogether(
            name='servicepackageservice',
            unique_together={('pkg', 'service')},
        ),
        migrations.AlterModelTable(
            name='inventorycategory',
            table='inventory_category',
        ),
    ]
