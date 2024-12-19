from django.contrib import admin
from .models import Customer_Data,Transaction,ElectricityPayment,WaterPayment,MobileRechargePayment,LoanApplication

# Register your models here.


class Customer_Data_Admin(admin.ModelAdmin):
    list_display = ('Cust_ID','Name','Phone_no','Email','Balance')
    list_filter = ('created', 'updated')  # Filters for easy searching by date
    search_fields = ('Name', 'Phone_no', 'Email', 'Cust_ID','Balance')  # Search bar for these fields
    ordering = ('-created',)  # Orders by newest customer created first
    readonly_fields = ('Cust_ID', 'created', 'updated')  # Prevents changes to these fields in the admin panel

admin.site.register(Customer_Data, Customer_Data_Admin)


class Transaction_Admin(admin.ModelAdmin):
    list_display = ('transaction_id', 'transaction_type', 'amount', 'customer', 'receiver', 'timestamp')
    list_filter = ('transaction_type', 'timestamp')  # Filters for easy searching
    search_fields = ('customer__Name', 'receiver__Name', 'transaction_id')  # Search by customer/receiver name or transaction ID
    date_hierarchy = 'timestamp'  # Adds a date drill-down filter
    ordering = ('-timestamp',)  # Orders transactions by most recent first


class BillPayment_Admin(admin.ModelAdmin):
    list_display = ('bill_type', 'amount', 'customer', 'paid_on', 'consumer_number', 'office', 'water_office', 'mobile_service_provider')
    list_filter = ('bill_type', 'paid_on', 'office', 'water_office', 'mobile_service_provider') 
    search_fields = ('customer__Name', 'consumer_number', 'bill_type')  
    date_hierarchy = 'paid_on' 
    ordering = ('-paid_on',)  

admin.site.register(Transaction, Transaction_Admin)

class ElectricityPayment_Admin(admin.ModelAdmin):
    list_display = ('customer', 'office', 'consumer_number', 'amount', 'paid_on')  # Fields to display in the list
    list_filter = ('office', 'paid_on')  # Filters for searching by office and date
    search_fields = ('customer__Name', 'consumer_number', 'office')  # Search by customer name, office, or consumer number
    ordering = ('-paid_on',)  # Orders by the most recent payment
    readonly_fields = ('customer', 'paid_on')  # Prevents changing the customer and paid_on fields

admin.site.register(ElectricityPayment, ElectricityPayment_Admin)


class WaterPayment_Admin(admin.ModelAdmin):
    list_display = ('customer', 'office', 'consumer_number', 'amount', 'paid_on')
    list_filter = ('office', 'paid_on')
    search_fields = ('customer__Name', 'consumer_number', 'office')
    ordering = ('-paid_on',)
    readonly_fields = ('customer', 'paid_on')

admin.site.register(WaterPayment, WaterPayment_Admin)


class MobileRechargePayment_Admin(admin.ModelAdmin):
    list_display = ('customer', 'service_provider', 'phone_number', 'amount', 'recharged_on')
    list_filter = ('service_provider', 'recharged_on')
    search_fields = ('customer__Name', 'phone_number', 'service_provider')
    ordering = ('-recharged_on',)
    readonly_fields = ('customer', 'recharged_on')

admin.site.register(MobileRechargePayment, MobileRechargePayment_Admin)

class LoanApplication_Admin(admin.ModelAdmin):
    list_display = ('customer', 'loan_type', 'loan_amount', 'interest_rate', 'tenure_years', 'applied_on')
    list_filter = ('loan_type', 'applied_on')
    search_fields = ('customer__Name', 'loan_type')
    ordering = ('-applied_on',)
    readonly_fields = ('customer', 'applied_on')

admin.site.register(LoanApplication, LoanApplication_Admin)

