# Generated by Django 5.0.4 on 2024-05-09 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0009_couponpurchase_expired_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='couponpurchase',
            name='expired_date',
        ),
    ]
