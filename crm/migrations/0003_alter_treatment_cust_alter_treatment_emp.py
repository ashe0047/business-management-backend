# Generated by Django 4.2 on 2023-05-19 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0004_alter_employeebankaccount_bank_acc_num_and_more'),
        ('crm', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treatment',
            name='cust',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='treatment', to='crm.customer'),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='emp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='treatment', to='hrm.employee'),
        ),
    ]
