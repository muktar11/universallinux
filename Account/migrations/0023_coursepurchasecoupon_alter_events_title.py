# Generated by Django 5.0.4 on 2024-05-14 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0022_rename_coupon_id_couponpurchase_course_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoursePurchaseCoupon',
            fields=[
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('coupon_code', models.CharField(blank=True, max_length=255, null=True)),
                ('course_id', models.CharField(blank=True, max_length=255, null=True)),
                ('student_id', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='events',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]