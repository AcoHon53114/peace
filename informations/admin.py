from django.contrib import admin

# Register your models here.
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'name', 'phone', 'email', 'visit_date','visit_time', 'submit_date')
    list_display_links = ('id', 'title', 'name')
    list_filter = ('title', 'name', 'phone', 'email', 'visit_date', 'visit_time')
    search_fields = ('title', 'name', 'phone', 'email')
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
    
admin.site.register(Booking, BookingAdmin)
