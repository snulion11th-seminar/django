# Generated by Django 4.1.7 on 2023-04-29 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_rename_tag_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='author',
        ),
    ]
