# Generated by Django 5.0.4 on 2024-05-10 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0016_rename_file_post_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='title',
        ),
    ]