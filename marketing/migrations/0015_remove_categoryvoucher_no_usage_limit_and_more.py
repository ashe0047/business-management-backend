# Generated by Django 4.2 on 2023-07-04 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0014_categoryvoucher_no_usage_limit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoryvoucher',
            name='no_usage_limit',
        ),
        migrations.RemoveField(
            model_name='genericvoucher',
            name='no_usage_limit',
        ),
        migrations.RemoveField(
            model_name='itemvoucher',
            name='no_usage_limit',
        ),
    ]