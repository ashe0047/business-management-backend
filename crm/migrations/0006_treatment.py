# Generated by Django 4.2 on 2023-07-11 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_alter_inventorycategory_options_and_more'),
        ('hrm', '0003_alter_bankdatabase_bank_name_and_more'),
        ('pos', '0014_rename_gen_voucher_used_sale_gen_voucher_use'),
        ('crm', '0005_delete_treatment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('treatment_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('treatment_date', models.DateTimeField()),
                ('treatment_notes', models.TextField(blank=True)),
                ('treatment_img', models.ImageField(upload_to='')),
                ('cust', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='treatment', to='crm.customer')),
                ('emp', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='treatment', to='hrm.employee')),
                ('pkg_sub', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='treatment', to='pos.packagesubscription')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.service')),
            ],
            options={
                'db_table': 'treatment',
            },
        ),
    ]
