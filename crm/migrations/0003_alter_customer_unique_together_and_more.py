# Generated by Django 4.2 on 2023-06-24 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0002_alter_employee_unique_together'),
        ('crm', '0002_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='customer',
            unique_together={('cust_email',), ('cust_nric',), ('cust_phone_num',)},
        ),
        migrations.AlterUniqueTogether(
            name='treatment',
            unique_together={('cust', 'emp')},
        ),
    ]