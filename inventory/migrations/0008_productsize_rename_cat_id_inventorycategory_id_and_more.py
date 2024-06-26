# Generated by Django 4.2 on 2023-08-04 19:18

from django.db import migrations, models
import django.db.models.deletion
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_alter_service_service_img_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit', models.CharField(max_length=25)),
            ],
            options={
                'db_table': 'product_size',
            },
        ),
        migrations.RenameField(
            model_name='inventorycategory',
            old_name='cat_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='inventorycategory',
            old_name='cat_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='inventorycategory',
            old_name='cat_type',
            new_name='type',
        ),
        migrations.AddField(
            model_name='product',
            name='prod_exp_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='prod_ingredients',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='inventorycategory',
            unique_together={('name',)},
        ),
        migrations.CreateModel(
            name='ProductBrand',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('desc', models.CharField(blank=True, max_length=300, null=True)),
                ('origin_country', models.CharField(blank=True, max_length=100, null=True)),
                ('ext_info', models.FileField(blank=True, null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to='inventory/products/brand/docs')),
            ],
            options={
                'db_table': 'product_brand',
                'unique_together': {('name',)},
            },
        ),
        migrations.AddField(
            model_name='product',
            name='prod_brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product', to='inventory.productbrand'),
        ),
        migrations.AddField(
            model_name='product',
            name='prod_size',
            field=models.ManyToManyField(related_name='product', to='inventory.productsize'),
        ),
    ]
