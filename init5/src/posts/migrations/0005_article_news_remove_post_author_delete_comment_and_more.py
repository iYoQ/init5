# Generated by Django 4.0.1 on 2022-01-10 04:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0004_alter_post_view_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('number_of_comments', models.IntegerField(default=0)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('rating', models.FloatField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)], default=0)),
                ('users_changed_rating', models.JSONField(default=dict, null=True)),
                ('active', models.BooleanField(default=True)),
                ('moderation', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
                'ordering': ('date_create',),
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('number_of_comments', models.IntegerField(default=0)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('rating', models.FloatField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)], default=0)),
                ('users_changed_rating', models.JSONField(default=dict, null=True)),
                ('active', models.BooleanField(default=True)),
                ('moderation', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
                'ordering': ('date_create',),
            },
        ),
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
