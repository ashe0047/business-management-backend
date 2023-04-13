# Generated by Django 4.1.7 on 2023-04-02 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pos', '0001_initial'),
        ('hrm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commission',
            fields=[
                ('com_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('com_amt', models.DecimalField(decimal_places=10, max_digits=1000)),
                ('com_date', models.DateField(blank=True, null=True)),
                ('com_type', models.CharField(blank=True, max_length=50, null=True)),
                ('emp', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hrm.employee')),
                ('sales_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.saleitem')),
            ],
            options={
                'db_table': 'commission',
            },
        ),
    ]
