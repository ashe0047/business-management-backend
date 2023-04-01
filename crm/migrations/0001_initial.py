# Generated by Django 4.1.7 on 2023-04-01 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('cust_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cust_name', models.CharField(max_length=150)),
                ('cust_phone_num', models.BigIntegerField(blank=True, null=True)),
                ('cust_address', models.CharField(blank=True, max_length=1000, null=True)),
                ('cust_dob', models.DateField(blank=True, null=True)),
                ('cust_email', models.CharField(blank=True, max_length=300, null=True)),
                ('cust_nric', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'customer',
                'unique_together': {('cust_phone_num', 'cust_nric', 'cust_name', 'cust_email')},
            },
        ),
    ]
