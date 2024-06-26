# Generated by Django 4.2 on 2023-06-23 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryCategory',
            fields=[
                ('cat_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cat_type', models.CharField(choices=[('product', 'Product'), ('service', 'Service')], max_length=15)),
                ('cat_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='servicepackage',
            name='pkg_discount_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
    ]
