# Generated by Django 4.2.4 on 2023-08-16 23:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurants', '0004_alter_menu_detail_content_alter_menu_detail_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openhours',
            name='close_time',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='phone',
            field=models.CharField(max_length=20, null=True, verbose_name='phone'),
        ),
    ]
