from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from .models import Customer_Data,Transaction,ElectricityPayment,WaterPayment,MobileRechargePayment,LoanApplication
from .form import UpdateAccountForm, CloseAccountForm,DepositForm,WithdrawForm,FundTransferForm,CustomSignupForm,ElectricityPaymentForm,WaterPaymentForm,MobileRechargePaymentForm,LoanApplicationForm
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator

# Create your views here.

# login_required
def home(request):
    # Fetch only the customer associated with the logged-in user
    customer = Customer_Data.objects.filter(Name=request.user.username)
    return render(request, "home.html", {'customers': customer})

@login_required(login_url='login')
def profile_view(request):
    customer = Customer_Data.objects.get(Name=request.user.username)
    return render(request, 'profile.html', {'customer': customer})

@login_required(login_url='login')
def check_balance(request):
    # Fetch the customer data of the logged-in user
    customer = get_object_or_404(Customer_Data, Name=request.user.username)
    
    # Pass the balance to the template
    context = {
        'balance': customer.Balance,

    }

    return render(request, 'check_balance.html', context)

#SIGNUP

def signup_user(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save()
            # Create the associated Customer_Data entry
            customer = Customer_Data.objects.create(
                Name=form.cleaned_data['name'],
                Email=form.cleaned_data['email'],
                Phone_no=form.cleaned_data['phone_no'],
                Balance=0.0  # Initial balance
            )
            messages.success(request, "Account created successfully. You can now log in.")
            return render(request, 'account_created.html', {'customer': customer})
    else:
        form = CustomSignupForm()

    return render(request, 'signup.html', {'form': form})


# login

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username = user_name, password = password)

            if user is not None:
                login(request, user)
                return redirect('home') # redicts to dashboard
            else:
                return render(request,'login.html', {'form': form})
            
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form} )


 #LOGOUT

def logout_user(request):
    logout(request)
    return redirect('login')   

# Update account view
@login_required(login_url='login')
def update_account(request, Cust_ID):
    customer = get_object_or_404(Customer_Data, Cust_ID=Cust_ID)
    if request.method == 'POST':
        form = UpdateAccountForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return render(request, 'update_sucess.html', {'customer': customer})
    else:
        form = UpdateAccountForm(instance=customer)
    return render(request, 'update_account.html', {'form': form, 'customer': customer})

# Close account view
@login_required(login_url='login')
def close_account(request, Cust_ID):
    customer = get_object_or_404(Customer_Data, Cust_ID=Cust_ID)
    if request.method == 'POST':
        form = CloseAccountForm(request.POST)
        if form.is_valid():
            # Delete customer account
            customer.delete()
            return render(request, 'close_success.html', {'Cust_ID': Cust_ID})
    else:
        form = CloseAccountForm()
    return render(request, 'close_account.html', {'form': form, 'customer': customer})


from django.utils.timezone import now

@login_required(login_url='login')
def deposit(request):
    customers = Customer_Data.objects.filter(Name=request.user.username)

    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            customer = get_object_or_404(Customer_Data, Name=request.user.username)
            amount = form.cleaned_data['amount']
            
            # Define the interest rate per quarter
            interest_rate = 0.02  # 2% quarterly interest

            # Get the last interest calculation date (default to account creation date)
            last_calculated_date = customer.last_interest_calculation or customer.created
            current_date = now()  # Use timezone-aware `now`

            # Calculate the number of quarters elapsed
            time_difference = current_date - last_calculated_date
            quarters_elapsed = time_difference.days // 90

            # Calculate interest if at least one quarter has passed
            interest = 0
            if quarters_elapsed > 0:
                interest = customer.Balance * (interest_rate * quarters_elapsed)
                customer.Balance += interest
                customer.last_interest_calculation = current_date

            # Add the deposited amount
            customer.Balance += amount
            customer.save()

            # Log the transaction
            Transaction.objects.create(transaction_type="Deposit", amount=amount, customer=customer)

            messages.success(
                request,
                f"Successfully deposited ₹{amount}. Interest of ₹{interest:.2f} added for {quarters_elapsed} quarter(s)."
            )
            return render(
                request,
                'deposit_success.html',
                {
                    'balance': customer.Balance,
                    'amount': amount,
                    'interest': interest,
                    'quarters': quarters_elapsed,
                    'total': customer.Balance,
                }
            )
    else:
        form = DepositForm()

    return render(request, 'deposit.html', {'form': form, 'customers': customers})

#Withdraw
@login_required(login_url='login')
def withdraw(request):
    customers = Customer_Data.objects.filter(Name=request.user.username)

    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            customer = get_object_or_404(Customer_Data, Name=request.user.username)
            amount = form.cleaned_data['amount']
            if customer.Balance >= amount:
                Transaction.objects.create(transaction_type="Withdraw", amount=amount, customer=customer)
                customer.Balance -= amount
                customer.save()
                messages.success(request, f"Successfully withdrew {amount}.")
                return render(request, 'withdraw_success.html', {'balance': customer.Balance, 'amount': amount})
            else:
                messages.error(request, "Insufficient balance.")
    else:
        form = WithdrawForm()
    return render(request, 'withdraw.html', {'form': form,'customers': customers})

@login_required(login_url='login')
def fund_transfer(request):
    customers = Customer_Data.objects.filter(Name=request.user.username)

    if request.method == 'POST':
        form = FundTransferForm(request.POST)
        form.fields['account_number'].queryset = Customer_Data.objects.exclude(Name=request.user.username).values_list('Cust_ID', flat=True)
 

        if form.is_valid():
            customer = get_object_or_404(Customer_Data, Name=request.user.username)
            account_number = form.cleaned_data['account_number']  # This now gives the Cust_ID (account number)
            amount = form.cleaned_data['amount']

            # Ensure the selected account number is not the same as the sender's account
            if account_number == customer.Cust_ID:
                messages.error(request, "You cannot transfer money to your own account.")
                return render(request, 'fund_transfer.html', {'form': form})

            # Check if the sender has sufficient balance
            if customer.Balance >= amount:
                # Get the recipient's account based on the Cust_ID (account number)
                recipient = get_object_or_404(Customer_Data, Cust_ID=account_number)
                
                # Create the transaction
                Transaction.objects.create(transaction_type="Transfer", amount=amount, customer=customer, receiver=recipient)
                
                # Update balances
                customer.Balance -= amount
                recipient.Balance += amount
                customer.save()
                recipient.save()

                # Redirect to the success page with updated balance
                return render(request, 'fund_transfer_success.html', {
                    'amount': amount,
                    'balance': customer.Balance,
                    'recipient_name': recipient.Name
                })
            else:
                messages.error(request, "Insufficient balance.")
    else:
        form = FundTransferForm()
        form.fields['account_number'].queryset = Customer_Data.objects.exclude(Name=request.user.username)

    return render(request, 'fund_transfer.html', {'form': form, 'customers': customers})

@login_required(login_url='login')
def get_recipient_details(request, account_number):
    # Fetch recipient details based on the provided account number (Cust_ID)
    try:
        recipient = Customer_Data.objects.get(Cust_ID=account_number)
        data = {
            'name': recipient.Name,
            'email': recipient.Email,
            'phone_no': recipient.Phone_no
        }
        return JsonResponse(data)
    except Customer_Data.DoesNotExist:
        return JsonResponse({'error': 'Recipient not found.'}, status=404)
    
@login_required(login_url='login')
def electricity_payment(request):
    customer = get_object_or_404(Customer_Data, Name=request.user.username)

    if request.method == 'POST':
        form = ElectricityPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.customer = customer

            if customer.Balance >= payment.amount:
                # Deduct the amount from the customer's balance
                customer.Balance -= payment.amount
                customer.save()

                # Save the electricity payment record
                payment.save()

                messages.success(request, "Electricity payment successful!")
                # Redirect to the receipt page
                return redirect('electricity_receipt',payment_id=payment.id)
            else:
                messages.error(request, "Insufficient balance.")
        else:
            messages.error(request, "Invalid input. Please correct the errors.")
    else:
        form = ElectricityPaymentForm()

    return render(request, 'electricity_payment.html', {'form': form})

@login_required(login_url='login')
def electricity_payment_history(request):
    customer = get_object_or_404(Customer_Data, Name=request.user.username)

    # Fetch all electricity payments for the logged-in customer
    electricity_payments = ElectricityPayment.objects.filter(customer=customer).order_by('-paid_on')

    # Set up pagination (10 payments per page)
    paginator = Paginator(electricity_payments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the data in the context
    context = {
        'page_obj': page_obj,  # Paginated data
    }
    return render(request, 'transaction_history.html', context)

@login_required(login_url='login')
def electricity_receipt(request, payment_id):
    # Fetch the electricity payment record
    payment = get_object_or_404(ElectricityPayment, id=payment_id)

    # Render the receipt template
    context = {
        'payment': payment,
        'customer': payment.customer,
    }
    return render(request, 'electricity_receipt.html', context)

@login_required(login_url='login')
def water_payment(request):
    customer = get_object_or_404(Customer_Data, Name=request.user.username)

    if request.method == 'POST':
        form = WaterPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.customer = customer

            if customer.Balance >= payment.amount:
                # Deduct the amount from the customer's balance
                customer.Balance -= payment.amount
                customer.save()

                # Save the water payment record
                payment.save()

                messages.success(request, "Water payment successful!")
                return redirect('water_receipt',payment_id=payment.id)
            else:
                messages.error(request, "Insufficient balance.")
        else:
            messages.error(request, "Invalid input. Please correct the errors.")
    else:
        form = WaterPaymentForm()

    return render(request, 'water_payment.html', {'form': form})

@login_required(login_url='login')
def water_payment_history(request):
    customer = get_object_or_404(Customer_Data, Name=request.user.username)

    # Fetch all water payments for the logged-in customer
    water_payments = WaterPayment.objects.filter(customer=customer).order_by('-paid_on')

    # Set up pagination (10 payments per page)
    paginator = Paginator(water_payments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,  # Paginated data
    }
    return render(request, 'transaction_history.html', context)

@login_required(login_url='login')
def water_receipt(request, payment_id):
    # Fetch the water payment record
    payment = get_object_or_404(WaterPayment, id=payment_id)

    # Render the receipt template
    context = {
        'payment': payment,
        'customer': payment.customer,
    }
    return render(request, 'water_receipt.html', context)

@login_required(login_url='login')
def mobile_recharge_payment(request):
    customer = get_object_or_404(Customer_Data, Name=request.user.username)

    if request.method == 'POST':
        form = MobileRechargePaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.customer = customer

            if customer.Balance >= payment.amount:
                # Deduct the amount from the customer's balance
                customer.Balance -= payment.amount
                customer.save()

                # Save the mobile recharge payment record
                payment.save()

                messages.success(request, "Mobile recharge successful!")
                return redirect('mobile_recharge_receipt',recharge_id=payment.id)
            else:
                messages.error(request, "Insufficient balance.")
        else:
            messages.error(request, "Invalid input. Please correct the errors.")
    else:
        form = MobileRechargePaymentForm()

    return render(request, 'recharge_payment.html', {'form': form})

@login_required(login_url='login')
def mobile_recharge_history(request):
    customer = get_object_or_404(Customer_Data, Name=request.user.username)

    # Fetch all mobile recharge payments for the logged-in customer
    mobile_recharges = MobileRechargePayment.objects.filter(customer=customer).order_by('-recharged_on')

    # Set up pagination (10 payments per page)
    paginator = Paginator(mobile_recharges, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,  # Paginated data
    }
    return render(request, 'transaction_history.html', context)

def mobile_recharge_receipt(request, recharge_id):
    # Get the mobile recharge payment
    recharge = get_object_or_404(MobileRechargePayment, id=recharge_id)

    # Prepare the receipt data
    context = {
        'recharge': recharge,
        'customer': recharge.customer,
    }

    # Render receipt in a separate template
    return render(request, 'mobile_recharge_receipt.html', context)


@login_required(login_url='login')
def display_all_payments_history(request):
    customer = get_object_or_404(Customer_Data, Name=request.user.username)

    # Query data for each table
    electricity_payments = ElectricityPayment.objects.filter(customer=customer).order_by('-paid_on')
    water_payments = WaterPayment.objects.filter(customer=customer).order_by('-paid_on')
    mobile_recharge_payments = MobileRechargePayment.objects.filter(customer=customer).order_by('-recharged_on')
    # Query data from Transaction table
    transactions = Transaction.objects.filter(customer=customer).order_by('-timestamp')


    # Set up pagination for each table
    electricity_paginator = Paginator(electricity_payments, 5)
    electricity_page_number = request.GET.get('electricity_page')
    electricity_page_obj = electricity_paginator.get_page(electricity_page_number)

    water_paginator = Paginator(water_payments, 5)
    water_page_number = request.GET.get('water_page')
    water_page_obj = water_paginator.get_page(water_page_number)

    mobile_paginator = Paginator(mobile_recharge_payments, 5)
    mobile_page_number = request.GET.get('mobile_page')
    mobile_page_obj = mobile_paginator.get_page(mobile_page_number)

    transaction_paginator = Paginator(transactions, 5)
    transaction_page_number = request.GET.get('transaction_page')
    transaction_page_obj = transaction_paginator.get_page(transaction_page_number)

    # Render data in context
    context = {
        'balance': customer.Balance,
        'electricity_page_obj': electricity_page_obj,
        'water_page_obj': water_page_obj,
        'mobile_page_obj': mobile_page_obj,
        'transaction_page_obj': transaction_page_obj  # Include transaction data in context
    }
    return render(request, 'transaction_history.html', context)

@login_required(login_url='login')
def apply_for_loan(request):
    customer = get_object_or_404(Customer_Data, Name=request.user.username)

    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.customer = customer
            loan.save()
            return redirect('loan_details')  # Redirect to loan details
    else:
        form = LoanApplicationForm()

    return render(request, 'loan_application_form.html', {'form': form, 'customer':customer})

@login_required(login_url='login')
def loan_details(request):
    customer = get_object_or_404(Customer_Data, Name=request.user.username)
    loans = LoanApplication.objects.filter(customer=customer)
    return render(request, 'loan_details.html', {'loans': loans,'customer':customer})