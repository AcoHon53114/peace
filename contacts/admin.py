from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'contact_date')
    list_display_links = ('id', 'name')
    list_filter = ('name', 'phone', 'email')
    search_fields = ('name', 'phone', 'email', 'contact_date')
    list_per_page = 25
    
        # disable "Add Contact" button
    def has_add_permission(self, request):
        return False
    
        # disable "Save" 和 "Save and continue editing" button
    def has_change_permission(self, request, obj=None):
        return False
    
        # disable "Delete" button
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Contact, ContactAdmin)



