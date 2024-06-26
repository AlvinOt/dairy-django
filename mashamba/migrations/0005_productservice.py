# Generated by Django 4.2.13 on 2024-06-25 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mashamba', '0004_remove_farm_products_services'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Fresh Milk', max_length=100)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_services', to='mashamba.farm')),
            ],
        ),
    ]
