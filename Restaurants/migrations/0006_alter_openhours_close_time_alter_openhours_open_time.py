# Generated by Django 4.2.4 on 2023-08-16 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurants', '0005_alter_openhours_close_time_alter_restaurant_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openhours',
            name='close_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='openhours',
            name='open_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
