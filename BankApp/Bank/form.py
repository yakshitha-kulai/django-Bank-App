
from django import forms
from .models import Customer_Data,Transaction,User,ElectricityPayment,WaterPayment,MobileRechargePayment,LoanApplication
from django.contrib.auth.forms import UserCreationForm

class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_no = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'name', 'phone_no']

# class CreateAccountForm(forms.ModelForm):
#     Name = forms.CharField(
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
#         required=True,
#         label="Full Name"
#     )

#     Phone_no = forms.CharField(
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
#         required=True,
#         label="Phone Number",
#         max_length=10,
#         min_length=10
#     )

#     Email = forms.EmailField(
#         widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
#         required=True,
#         label="Email Address"
#     )

#     class Meta:
#         model = Customer_Data
#         fields = ['Name', 'Phone_no', 'Email']



# Form for updating account details
class UpdateAccountForm(forms.ModelForm):
    Name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Update name'}),
        required=True,
        label="Full Name"
    )

    Phone_no = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Update phone number'}),
        required=True,
        label="Phone Number",
        max_length=10,
        min_length=10
    )

    Email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Update email address'}),
        required=True,
        label="Email Address"
    )

    class Meta:
        model = Customer_Data
        fields = ['Name', 'Phone_no', 'Email']



# Form for account closure confirmation
class CloseAccountForm(forms.Form):
    confirm = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="I confirm that I want to close this account"
    )


class DepositForm(forms.ModelForm):
    amount = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,
    )

    class Meta:
        model = Transaction
        fields = ['amount']

class WithdrawForm(forms.ModelForm):
    amount = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,
    )

    class Meta:
        model = Transaction
        fields = ['amount']

class ElectricityPaymentForm(forms.ModelForm):
    class Meta:
        model = ElectricityPayment
        fields = ['office', 'consumer_number', 'amount']
        widgets = {
            'office': forms.Select(attrs={'class': 'form-control'}),
            'consumer_number': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class WaterPaymentForm(forms.ModelForm):
    class Meta:
        model = WaterPayment
        fields = ['office', 'consumer_number', 'amount']
        widgets = {
            'office': forms.Select(attrs={'class': 'form-control'}),
            'consumer_number': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class MobileRechargePaymentForm(forms.ModelForm):
    class Meta:
        model = MobileRechargePayment
        fields = ['service_provider', 'phone_number', 'amount']
        widgets = {
            'service_provider': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
class FundTransferForm(forms.Form):
    account_number = forms.ModelChoiceField(
        queryset=Customer_Data.objects.all(),  # Include all customers
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        to_field_name='Cust_ID'  # This ensures you fetch only the Cust_ID field
    )
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Amount to Transfer"
    )
    class Meta:
        model = Transaction
        fields = ['account_number', 'amount']

class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = [
            'loan_type', 'loan_amount', 'interest_rate', 'tenure_years'
        ]
        widgets = {
            'loan_type': forms.Select(attrs={'class': 'form-control'}),
            'loan_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'tenure_years': forms.NumberInput(attrs={'class': 'form-control'}),
        }
