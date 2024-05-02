# Generated by Django 5.0.2 on 2024-04-26 13:55

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_image_options_remove_image_image_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=True, quality=75, scale=None, size=[500, 300], upload_to='post_images/'),
        ),
    ]