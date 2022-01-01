# Generated by Django 4.0 on 2021-12-27 05:25

import django.core.validators
from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('username', models.CharField(max_length=25, unique=True)),
                ('date_registration', models.DateTimeField(auto_now_add=True, verbose_name='date registration')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('role', models.CharField(blank=True, choices=[('user', 'user'), ('admin', 'admin')], default='user', max_length=100, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('is_newsmaker', models.BooleanField(default=False)),
                ('hide_email', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ['id'],
            },
            managers=[
                ('objects', users.models.UserManager()),
            ],
        ),
    ]
