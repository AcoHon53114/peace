from django.contrib import admin

# Register your models here.
from .models import Bank

class BankAdmin(admin.ModelAdmin):
    list_display = ('resident_id', 'resident_name', 'payment_method', 'submit_date')
    list_display_links = ('resident_id', 'resident_name', 'payment_method')
    list_filter = ('resident_id', 'resident_name', 'payment_method',)
    search_fields = ('resident_id', 'resident_name', 'payment_method',)
    list_per_page = (25)
    
admin.site.register(Bank, BankAdmin)