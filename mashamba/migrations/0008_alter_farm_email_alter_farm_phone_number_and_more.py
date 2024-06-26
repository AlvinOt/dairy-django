# Generated by Django 4.2.13 on 2024-06-25 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mashamba', '0007_alter_productservice_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farm',
            name='email',
            field=models.EmailField(blank=True, default='dairydose@gmail.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='farm',
            name='phone_number',
            field=models.CharField(blank=True, default='0704644959', max_length=20),
        ),
        migrations.AlterField(
            model_name='farm',
            name='slogan',
            field=models.CharField(blank=True, default='We Care', help_text='Farm motto', max_length=255),
        ),
    ]
