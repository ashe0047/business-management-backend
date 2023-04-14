# Generated by Django 4.1.7 on 2023-04-14 06:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('emp_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('emp_name', models.CharField(max_length=150)),
                ('emp_dob', models.DateField()),
                ('emp_address', models.CharField(max_length=1000)),
                ('emp_nric', models.BigIntegerField()),
                ('emp_phone_num', models.BigIntegerField()),
                ('emp_salary', models.DecimalField(decimal_places=10, max_digits=1000)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'employee',
                'unique_together': {('emp_name', 'emp_nric', 'emp_phone_num')},
            },
        ),
        migrations.CreateModel(
            name='EmployeeBenefitAccount',
            fields=[
                ('benefit_acc_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('benefit_acc_name', models.CharField(max_length=150)),
                ('benefit_acc_type', models.CharField(max_length=100)),
                ('benefit_acc_num', models.BigIntegerField()),
                ('emp', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employeebenefitaccount', to='hrm.employee')),
            ],
            options={
                'db_table': 'employee_benefit_account',
                'unique_together': {('emp', 'benefit_acc_num')},
            },
        ),
        migrations.CreateModel(
            name='EmployeeBankAccount',
            fields=[
                ('bank_acc_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('bank_name', models.CharField(max_length=150)),
                ('bank_acc_num', models.BigIntegerField()),
                ('bank_acc_type', models.CharField(max_length=100)),
                ('bank_routing_num', models.IntegerField(blank=True, null=True)),
                ('emp', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employeebankaccount', to='hrm.employee')),
            ],
            options={
                'db_table': 'employee_bank_account',
                'unique_together': {('bank_acc_num', 'emp')},
            },
        ),
    ]
