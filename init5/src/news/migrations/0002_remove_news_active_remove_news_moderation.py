# Generated by Django 4.0.1 on 2022-01-16 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='active',
        ),
        migrations.RemoveField(
            model_name='news',
            name='moderation',
        ),
    ]