# Generated by Django 3.1.1 on 2021-06-18 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0009_auto_20210618_1055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='protocol',
            old_name='bus_type',
            new_name='type',
        ),
    ]