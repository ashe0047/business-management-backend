# Generated by Django 4.1.7 on 2023-04-04 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0002_employee_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='user_id',
            new_name='user',
        ),
    ]