# Generated by Django 4.1.7 on 2023-04-23 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pos', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commission',
            name='sales_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.saleitem'),
        ),
    ]