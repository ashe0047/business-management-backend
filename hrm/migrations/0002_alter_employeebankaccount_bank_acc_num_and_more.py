# Generated by Django 4.1.7 on 2023-03-27 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hrm", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employeebankaccount",
            name="bank_acc_num",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="employeebenefitaccount",
            name="benefit_acc_num",
            field=models.BigIntegerField(),
        ),
    ]
