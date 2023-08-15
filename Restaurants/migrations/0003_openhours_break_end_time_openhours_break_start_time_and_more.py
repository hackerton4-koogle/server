# Generated by Django 4.2.4 on 2023-08-14 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurants', '0002_alter_category_image_alter_food_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='openhours',
            name='break_end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='openhours',
            name='break_start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='openhours',
            name='last_order_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='koogle_ranking',
            field=models.IntegerField(default=0, verbose_name='koogle_ranking'),
        ),
    ]