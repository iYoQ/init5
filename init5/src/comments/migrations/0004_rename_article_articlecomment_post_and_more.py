# Generated by Django 4.0.1 on 2022-01-17 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_rename_post_articlecomment_article_and_more'),
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
    ]
