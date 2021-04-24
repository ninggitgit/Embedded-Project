# Generated by Django 3.1.1 on 2021-04-24 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.TextField(default='', unique=True)),
                ('item_content', models.TextField(default='')),
                ('item_describe', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Personnel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='')),
                ('age', models.IntegerField(blank=True, default=0)),
                ('gender', models.TextField(blank=True, default='')),
                ('account', models.TextField(default='', unique=True)),
                ('password', models.TextField(default='')),
                ('authority', models.IntegerField(default='')),
                ('team', models.TextField(blank=True, default='')),
            ],
        ),
    ]
