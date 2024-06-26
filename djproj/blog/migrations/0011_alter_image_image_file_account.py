# Generated by Django 5.0.2 on 2024-05-23 08:13

import blog.others
import django.db.models.deletion
import django_resized.forms
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_image_image_file'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=True, max_length=500, quality=75, scale=None, size=[500, 300], upload_to=blog.others.upload_to_author_directory),
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateTimeField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('photo', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[1920, 1080], upload_to='')),
                ('job', models.CharField(blank=True, max_length=250, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
