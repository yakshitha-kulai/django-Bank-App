# Generated by Django 5.1.3 on 2024-12-10 05:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bank', '0008_billpayment_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectricityPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('office', models.CharField(choices=[('MESCOM', 'MESCOM'), ('HESCOM', 'HESCOM'), ('BESCOM', 'BESCOM'), ('CHESCOM', 'CHESCOM'), ('GESCOM', 'GESCOM')], max_length=50)),
                ('consumer_number', models.CharField(max_length=15)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('paid_on', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bank.customer_data')),
            ],
        ),
    ]
