# Generated by Django 5.0.2 on 2024-04-19 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_remove_post_reading_time_post_readingtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='readingtime',
            field=models.PositiveBigIntegerField(max_length=100),
        ),
    ]
