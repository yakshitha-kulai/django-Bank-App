# Generated by Django 5.1.3 on 2024-12-14 10:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bank', '0019_remove_transaction_electricity_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_type', models.CharField(choices=[('Home Loan', 'Home Loan'), ('Vehicle Loan', 'Vehicle Loan'), ('Gold Loan', 'Gold Loan'), ('Education Loan', 'Education Loan')], max_length=20)),
                ('loan_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tenure_years', models.PositiveIntegerField()),
                ('collateral_details', models.TextField(blank=True, null=True)),
                ('education_details', models.TextField(blank=True, null=True)),
                ('vehicle_details', models.TextField(blank=True, null=True)),
                ('property_details', models.TextField(blank=True, null=True)),
                ('applied_on', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bank.customer_data')),
            ],
        ),
    ]