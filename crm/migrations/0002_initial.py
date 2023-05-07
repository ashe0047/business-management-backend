# Generated by Django 4.1.7 on 2023-04-23 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pos', '0001_initial'),
        ('crm', '0001_initial'),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='treatment',
            name='pkg_sub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.packagesubscription'),
        ),
        migrations.AddField(
            model_name='treatment',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.service'),
        ),
        migrations.AlterUniqueTogether(
            name='customer',
            unique_together={('cust_phone_num', 'cust_nric', 'cust_name', 'cust_email')},
        ),
    ]