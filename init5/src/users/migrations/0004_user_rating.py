# Generated by Django 4.0.1 on 2022-01-16 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]