# Generated by Django 4.1.7 on 2023-03-27 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0004_alter_customer_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="customer",
            unique_together={
                ("cust_phone_num", "cust_nric", "cust_name", "cust_email")
            },
        ),
    ]
