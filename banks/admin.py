from django.contrib import admin
from django.utils.timezone import localtime
# Register your models here.
from .models import Bank

class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'resident_code', 'resident_name', 'payment_method', 'payment_year', 'payment_month', 'depositslip_photo', 'uploaded_date')
    list_display_links = ('resident_code', 'resident_name', 'payment_method', 'payment_year', 'payment_month')
    list_filter = ('resident_code', 'resident_name', 'payment_method', 'payment_year', 'payment_month')
    search_fields = ('resident_code', 'resident_name', 'payment_method', 'payment_month', 'payment_year')
    list_per_page = (25)
    
        # disable "Add Contact" button
    def has_add_permission(self, request):
        return False
    
        # disable "Save" 和 "Save and continue editing" button
    def has_change_permission(self, request, obj=None):
        return False
    
        # disable "Delete" button
    def has_delete_permission(self, request, obj=None):
        return False
    
admin.site.register(Bank, BankAdmin)