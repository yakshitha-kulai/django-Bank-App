from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Customer_Data(models.Model):
    Cust_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    Phone_no = models.CharField(max_length=10)
    Email = models.EmailField()
    Balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    last_interest_calculation = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Name} ({self.Cust_ID})" 


class ElectricityPayment(models.Model):
    customer = models.ForeignKey(Customer_Data, on_delete=models.CASCADE)
    office = models.CharField(max_length=50, choices=[
        ('MESCOM', 'MESCOM'),
        ('HESCOM', 'HESCOM'),
        ('BESCOM', 'BESCOM'),
        ('CHESCOM', 'CHESCOM'),
        ('GESCOM', 'GESCOM'),
    ])
    consumer_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer.Name} - {self.office} - {self.amount}'


class WaterPayment(models.Model):
    customer = models.ForeignKey(Customer_Data, on_delete=models.CASCADE)
    office = models.CharField(max_length=50, choices=[
        ('Mangaluru', 'Mangaluru'),
        ('Bengaluru', 'Bengaluru'),
        ('Mysuru', 'Mysuru'),
    ])
    consumer_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.customer.Name} - {self.office} - {self.amount}'

class MobileRechargePayment(models.Model):
    customer = models.ForeignKey(Customer_Data, on_delete=models.CASCADE)
    service_provider = models.CharField(max_length=50, choices=[
        ('Jio', 'Jio'),
        ('BSNL', 'BSNL'),
        ('Airtel', 'Airtel'),
    ])
    phone_number = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    recharged_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer.Name} - {self.service_provider} - {self.amount}'

    
class BillPayment(models.Model):
    BILL_CHOICES = [
        ('Electricity', 'Electricity'),
        ('Water', 'Water'),
        ('Mobile Recharge', 'Mobile Recharge'),
    ]
    
    bill_type = models.CharField(max_length=20, choices=BILL_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    customer = models.ForeignKey(Customer_Data, on_delete=models.CASCADE)
    paid_on = models.DateTimeField(auto_now_add=True)
    
    # For Electricity Bills
    electricity_offices = [
        ('MESCOM', 'MESCOM'),
        ('HESCOM', 'HESCOM'),
        ('BESCOM', 'BESCOM'),
        ('CHESCOM', 'CHESCOM'),
        ('GESCOM', 'GESCOM'),
    ]
    office = models.CharField(max_length=10, choices=electricity_offices, blank=True, null=True)

    # For Water Bills
    water_offices = [
        ('Mangaluru', 'Mangaluru'),
        ('Bengaluru', 'Bengaluru'),
        ('Mysuru', 'Mysuru'),
    ]
    water_office = models.CharField(max_length=20, choices=water_offices, blank=True, null=True)

    # For Mobile Recharge Bills
    mobile_service_providers = [
        ('Jio', 'Jio'),
        ('BSNL', 'BSNL'),
        ('Airtel', 'Airtel'),
    ]
    mobile_service_provider = models.CharField(max_length=20, choices=mobile_service_providers, blank=True, null=True)
    
    consumer_number = models.CharField(max_length=6)

    phone_number = models.CharField(max_length=10, blank=True, null=True)  # Phone number for recharge


    def __str__(self):
        return f'{self.bill_type} - {self.amount} paid by {self.customer.Name}'    

class Transaction(models.Model):
    TRANSACTION_CHOICES = [
        ('Deposit', 'Deposit'),
        ('Withdraw', 'Withdraw'),
        ('Transfer', 'Transfer')
        
    ]

    transaction_id = models.AutoField(primary_key=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    customer = models.ForeignKey(Customer_Data, on_delete=models.CASCADE, related_name="transactions")
    receiver = models.ForeignKey(Customer_Data, on_delete=models.CASCADE, null=True, blank=True, related_name="received_transactions")
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        receiver_info = f" to {self.receiver.Name}" if self.receiver else ""
        return f'{self.transaction_type} - {self.amount} by {self.customer.Name}{receiver_info}'
    

class LoanApplication(models.Model):
    LOAN_TYPES = [
        ('Home Loan', 'Home Loan'),
        ('Vehicle Loan', 'Vehicle Loan'),
        ('Gold Loan', 'Gold Loan'),
        ('Education Loan', 'Education Loan'),
    ]

    customer = models.ForeignKey('Customer_Data', on_delete=models.CASCADE)  # Link to the customer model
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tenure_years = models.PositiveIntegerField()
    applied_on = models.DateTimeField(auto_now_add=True)

    def total_amount_payable(self):
        """Calculate the total amount payable."""
        return self.loan_amount + (self.loan_amount * self.interest_rate / 100) * self.tenure_years

    def __str__(self):
        return f"{self.customer} - {self.loan_type} - ₹{self.loan_amount}"
