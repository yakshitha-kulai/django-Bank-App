# Generated by Django 5.1.3 on 2024-12-11 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bank', '0014_alter_transaction_transaction_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='mobile_recharge_payment',
        ),
    ]
