# Generated by Django 4.2 on 2023-08-05 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_alter_product_prod_ingredients_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='prod_sku',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
