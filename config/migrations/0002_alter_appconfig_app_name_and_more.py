# Generated by Django 4.2 on 2023-06-24 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appconfig',
            name='app_name',
            field=models.CharField(choices=[('auth_core', 'auth_core'), ('core', 'core'), ('crm', 'crm'), ('hrm', 'hrm'), ('inventory', 'inventory'), ('pos', 'pos'), ('marketing', 'marketing'), ('store', 'store'), ('config', 'config'), ('general', 'general')], max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='appconfig',
            unique_together={('config_key', 'app_name')},
        ),
    ]
