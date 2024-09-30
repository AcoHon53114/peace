from django.contrib import admin

# Register your models here.
from .models import Bank

class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'resident_code', 'resident_name', 'payment_method', 'payment_year', 'payment_month', 'depositslip_photo', 'uploaded_date')
    list_display_links = ('resident_code', 'resident_name', 'payment_method', 'payment_year', 'payment_month')
    list_filter = ('resident_code', 'resident_name', 'payment_method', 'payment_year', 'payment_month')
    search_fields = ('resident_code', 'resident_name', 'payment_method', 'payment_month', 'payment_year')
    list_per_page = (25)
    
admin.site.register(Bank, BankAdmin)