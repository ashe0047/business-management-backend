# Generated by Django 4.2 on 2023-05-22 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_servicepackage_service'),
        ('pos', '0004_remove_packagesubscription_payment_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagesubscription',
            name='service',
            field=models.ManyToManyField(related_name='packagesubscription', through='pos.PackageSubscriptionService', to='inventory.service'),
        ),
    ]