# Generated by Django 4.2.13 on 2024-06-25 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mashamba', '0002_farm_email_farm_phone_number_alter_cow_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='farm',
            name='products_services',
            field=models.CharField(default='Fresh Milk', max_length=100),
        ),
    ]