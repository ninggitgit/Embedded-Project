# Generated by Django 3.1.1 on 2021-06-19 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0011_variable'),
    ]

    operations = [
        migrations.AddField(
            model_name='variable',
            name='describe',
            field=models.TextField(default=''),
        ),
    ]