# Generated by Django 4.2 on 2023-08-05 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0021_alter_product_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('prod_sku',), ('prod_barcode',), ('prod_name', 'prod_category', 'prod_variant', 'prod_unit_size', 'prod_package_size', 'prod_weight')},
        ),
    ]
