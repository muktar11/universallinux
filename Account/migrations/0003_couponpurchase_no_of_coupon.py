# Generated by Django 5.0.4 on 2024-05-08 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0002_couponpurchase'),
    ]

    operations = [
        migrations.AddField(
            model_name='couponpurchase',
            name='no_of_coupon',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
