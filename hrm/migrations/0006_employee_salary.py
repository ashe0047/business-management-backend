# Generated by Django 4.1.7 on 2023-04-09 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0005_alter_employee_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='salary',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=1000, null=True),
        ),
    ]
