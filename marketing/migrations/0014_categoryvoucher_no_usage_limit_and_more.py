# Generated by Django 4.2 on 2023-07-04 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0013_alter_categoryvoucher_voucher_sale_discount_percent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoryvoucher',
            name='no_usage_limit',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='genericvoucher',
            name='no_usage_limit',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='itemvoucher',
            name='no_usage_limit',
            field=models.BooleanField(default=False),
        ),
    ]