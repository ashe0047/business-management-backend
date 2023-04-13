# Generated by Django 4.1.7 on 2023-04-09 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0006_employee_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeebankaccount',
            name='emp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employeebankaccount', to='hrm.employee'),
        ),
        migrations.AlterField(
            model_name='employeebenefitaccount',
            name='emp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employeebenefitaccount', to='hrm.employee'),
        ),
    ]
