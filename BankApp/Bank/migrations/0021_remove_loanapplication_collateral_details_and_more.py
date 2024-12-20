# Generated by Django 5.1.3 on 2024-12-15 05:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bank', '0020_loanapplication'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanapplication',
            name='collateral_details',
        ),
        migrations.RemoveField(
            model_name='loanapplication',
            name='education_details',
        ),
        migrations.RemoveField(
            model_name='loanapplication',
            name='property_details',
        ),
        migrations.RemoveField(
            model_name='loanapplication',
            name='vehicle_details',
        ),
        migrations.AddField(
            model_name='customer_data',
            name='last_interest_calculation',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
