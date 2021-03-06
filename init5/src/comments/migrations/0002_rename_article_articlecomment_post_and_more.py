# Generated by Django 4.0.1 on 2022-01-16 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articlecomment',
            old_name='article',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='newscomment',
            old_name='news',
            new_name='post',
        ),
        migrations.AlterField(
            model_name='articlecomment',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='newscomment',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
