# Generated by Django 5.0.2 on 2024-03-24 00:39

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='پیام')),
                ('name', models.CharField(max_length=250, verbose_name='نام ')),
                ('email', models.EmailField(max_length=254, verbose_name='ایمیل')),
                ('phone', models.CharField(max_length=11, verbose_name='شماره تماس')),
                ('subject', models.CharField(max_length=250, verbose_name='موضوع')),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='Status',
        ),
        migrations.RemoveField(
            model_name='post',
            name='auther',
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey( on_delete=django.db.models.deletion.CASCADE, related_name='user_posts', to=settings.AUTH_USER_MODEL,null=True,blank=True,verbose_name='نویسنده'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ انتشار'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=200, verbose_name='عنوان'),
        ),
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('DF', 'Draft'), ('PB', 'Published'), ('RG', 'Rejected')], default='DF', max_length=225, verbose_name='وضعیت'),
        ),
        migrations.RunSQL("UPDATE blog_post SET author_id = (SELECT id FROM auth_user WHERE username = 'nima') WHERE author_id IS NULL;"),#

        # Add the following lines
        migrations.AlterField(#
            model_name='post',#
            name='author',#
            field=models.ForeignKey(#
                to='auth.User',#
                on_delete=models.CASCADE,#
            ),
        ),
    ]
