from django.contrib import admin

# Register your models here.
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'name', 'phone', 'email', 'visit_date','visit_time', 'submit_date')
    list_display_links = ('id', 'title')
    list_filter = ('title', 'name', 'phone', 'email', 'visit_date', 'visit_time')
    search_fields = ('title', 'name', 'phone', 'email')
    list_per_page = (25)
    
admin.site.register(Booking, BookingAdmin)
