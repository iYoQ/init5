# Generated by Django 4.0.1 on 2022-01-19 00:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0006_rename_article_articlecomment_post_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articlecomment',
            old_name='post',
            new_name='article',
        ),
        migrations.RenameField(
            model_name='newscomment',
            old_name='post',
            new_name='news',
        ),
    ]
