# Generated by Django 4.2 on 2023-06-28 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0009_alter_sale_gross_sales_amt_alter_sale_net_sales_amt_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleitem',
            name='voucher_use_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
