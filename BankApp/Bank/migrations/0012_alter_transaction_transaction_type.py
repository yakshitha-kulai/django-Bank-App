# Generated by Django 5.1.3 on 2024-12-10 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bank', '0011_mobilerechargepayment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('Deposit', 'Deposit'), ('Withdraw', 'Withdraw'), ('Transfer', 'Transfer'), ('Electricity Payment', 'Electricity Payment'), ('Water Payment', 'Water Payment'), ('Mobile Recharge', 'Mobile Recharge')], max_length=20),
        ),
    ]
