from django.contrib import admin
from django.urls import path
from .views import home, login_user, signup_user, logout_user,update_account,close_account,deposit,withdraw,fund_transfer,get_recipient_details,electricity_payment,display_all_payments_history,mobile_recharge_payment,water_payment,mobile_recharge_receipt,electricity_receipt,water_receipt,profile_view,check_balance,apply_for_loan,loan_details

urlpatterns = [
    path('', home, name ="home"),
    path('login', login_user, name='login'),
    path('signup', signup_user, name='signup'),
    path('logout', logout_user, name='logout'),
    path('account/update/<int:Cust_ID>', update_account, name='update_account'),
    path('account/close/<int:Cust_ID>', close_account, name='close_account'),
    path('services/deposit', deposit, name='deposit'),
    path('services/withdraw', withdraw, name='withdraw'),
    path('services/fund_transfer', fund_transfer, name='fund_transfer'),
    path('history', display_all_payments_history, name='transaction_history'),
    path('get-recipient-details/<int:account_number>', get_recipient_details, name='get_recipient_details'),
    path('electricity', electricity_payment, name='electricity'),
    path('water', water_payment, name='water'),
    path('recharge', mobile_recharge_payment, name='recharge'),
    path('recharge/receipt/<int:recharge_id>', mobile_recharge_receipt, name='mobile_recharge_receipt'),
    path('electricity/receipt/<int:payment_id>', electricity_receipt, name='electricity_receipt'),
    path('water/receipt/<int:payment_id>/', water_receipt, name='water_receipt'),
    path('profile', profile_view, name='profile'),
    path('check-balance/', check_balance, name='check_balance'),
    path('loan/apply', apply_for_loan, name='loan'),
    path('loan/loandetails', loan_details, name='loan_details')


]

 
