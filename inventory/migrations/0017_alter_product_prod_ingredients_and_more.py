# Generated by Django 4.2 on 2023-08-05 18:57

from django.db import migrations, models
import inventory.models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0016_alter_inventorycategory_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='prod_ingredients',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='prod_sku',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]
