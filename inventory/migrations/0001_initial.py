# Generated by Django 4.1.7 on 2023-04-01 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('service_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('service_name', models.CharField(max_length=300)),
                ('service_desc', models.TextField(blank=True, null=True)),
                ('service_category', models.CharField(blank=True, max_length=100, null=True)),
                ('service_price', models.DecimalField(blank=True, decimal_places=10, max_digits=1000, null=True)),
                ('service_img', models.BinaryField(blank=True, null=True)),
            ],
            options={
                'db_table': 'service',
                'unique_together': {('service_name',)},
            },
        ),
        migrations.CreateModel(
            name='ProductSupplier',
            fields=[
                ('supplier_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('supplier_name', models.CharField(max_length=300)),
                ('supplier_contact', models.BigIntegerField(blank=True, null=True)),
                ('supplier_addres', models.CharField(blank=True, max_length=1000, null=True)),
                ('supplier_acc_num', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'product_supplier',
                'unique_together': {('supplier_name', 'supplier_acc_num')},
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('prod_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('prod_name', models.CharField(max_length=300)),
                ('prod_desc', models.TextField(blank=True, null=True)),
                ('prod_category', models.CharField(blank=True, max_length=100, null=True)),
                ('prod_price', models.DecimalField(blank=True, decimal_places=10, max_digits=1000, null=True)),
                ('prod_qty', models.IntegerField(blank=True, null=True)),
                ('prod_img', models.BinaryField(blank=True, null=True)),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.productsupplier')),
            ],
            options={
                'db_table': 'product',
                'unique_together': {('prod_name',)},
            },
        ),
    ]
