# Generated by Django 5.0.4 on 2024-05-12 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0017_remove_video_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
