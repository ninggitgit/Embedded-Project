# Generated by Django 3.1.1 on 2021-06-20 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0014_remove_testdata_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='protocol',
            name='refresh_cycle',
        ),
    ]