# Generated by Django 4.2 on 2023-06-23 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_inventorycategory_and_more'),
        ('marketing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericVoucher',
            fields=[
                ('voucher_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='marketing.voucher')),
            ],
            options={
                'db_table': 'generic_voucher',
            },
            bases=('marketing.voucher',),
        ),
        migrations.RenameField(
            model_name='voucher',
            old_name='voucher_associated_custs',
            new_name='cust',
        ),
        migrations.RemoveField(
            model_name='voucher',
            name='voucher_associated_products',
        ),
        migrations.RemoveField(
            model_name='voucher',
            name='voucher_associated_servicepkgs',
        ),
        migrations.RemoveField(
            model_name='voucher',
            name='voucher_associated_services',
        ),
        migrations.AddField(
            model_name='voucher',
            name='voucher_discount_amt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='voucher',
            name='voucher_discount_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.CreateModel(
            name='ItemVoucher',
            fields=[
                ('voucher_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='marketing.voucher')),
                ('pkg', models.ManyToManyField(blank=True, related_name='itemvoucher', to='inventory.servicepackage')),
                ('prod', models.ManyToManyField(blank=True, related_name='itemvoucher', to='inventory.product')),
                ('service', models.ManyToManyField(blank=True, related_name='itemvoucher', to='inventory.service')),
            ],
            options={
                'db_table': 'item_voucher',
            },
            bases=('marketing.voucher',),
        ),
        migrations.CreateModel(
            name='CategoryVoucher',
            fields=[
                ('voucher_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='marketing.voucher')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='categoryvoucher', to='inventory.inventorycategory')),
            ],
            options={
                'db_table': 'category_voucher',
            },
            bases=('marketing.voucher',),
        ),
    ]
