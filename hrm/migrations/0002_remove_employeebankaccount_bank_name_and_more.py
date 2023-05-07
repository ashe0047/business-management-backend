# Generated by Django 4.1.7 on 2023-04-25 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_bankdatabase'),
        ('hrm', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeebankaccount',
            name='bank_name',
        ),
        migrations.RemoveField(
            model_name='employeebankaccount',
            name='bank_routing_num',
        ),
        migrations.AddField(
            model_name='employeebankaccount',
            name='bank',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='core.bankdatabase'),
            preserve_default=False,
        ),
    ]
