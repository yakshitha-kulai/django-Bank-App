# Generated by Django 5.1.3 on 2024-12-11 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bank', '0013_transaction_mobile_recharge_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('Deposit', 'Deposit'), ('Withdraw', 'Withdraw'), ('Transfer', 'Transfer')], max_length=20),
        ),
    ]