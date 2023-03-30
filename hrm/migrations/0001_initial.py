# Generated by Django 4.1.7 on 2023-03-27 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Employee",
            fields=[
                ("emp_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("emp_name", models.CharField(blank=True, max_length=150, null=True)),
                ("emp_dob", models.DateField(blank=True, null=True)),
                (
                    "emp_address",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                ("emp_nric", models.BigIntegerField(blank=True, null=True)),
                ("empy_phone_num", models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "employee",
            },
        ),
        migrations.CreateModel(
            name="EmployeeBenefitAccount",
            fields=[
                (
                    "benefit_acc_id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("benefit_acc_name", models.CharField(max_length=150)),
                (
                    "benefit_acc_type",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("benefit_acc_num", models.IntegerField()),
                (
                    "emp",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="hrm.employee"
                    ),
                ),
            ],
            options={
                "db_table": "employee_benefit_account",
                "unique_together": {("benefit_acc_id", "emp", "benefit_acc_num")},
            },
        ),
        migrations.CreateModel(
            name="EmployeeBankAccount",
            fields=[
                ("bank_acc_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("bank_name", models.CharField(blank=True, max_length=150, null=True)),
                ("bank_acc_num", models.IntegerField(blank=True, null=True)),
                (
                    "bank_acc_type",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("bank_routing_num", models.IntegerField(blank=True, null=True)),
                (
                    "emp",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="hrm.employee"
                    ),
                ),
            ],
            options={
                "db_table": "employee_bank_account",
                "unique_together": {("bank_acc_num", "emp", "bank_acc_id")},
            },
        ),
    ]
