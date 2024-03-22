# Generated by Django 4.2 on 2023-08-04 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_alter_product_prod_sku_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbrand',
            name='sku_part',
            field=models.CharField(default='NA', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productsize',
            name='sku_part',
            field=models.CharField(default='NA', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productvariant',
            name='sku_part',
            field=models.CharField(default='NA', max_length=10),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='product',
            name='prod_size',
        ),
        migrations.CreateModel(
            name='ProductWeight',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit', models.CharField(max_length=25)),
                ('sku_part', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'product_weight',
                'unique_together': {('value', 'unit')},
            },
        ),
        migrations.AddField(
            model_name='product',
            name='prod_weight',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product', to='inventory.productweight'),
        ),
        migrations.AddField(
            model_name='product',
            name='prod_size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product', to='inventory.productsize'),
        ),
    ]
