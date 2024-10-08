from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'contact_date')
    list_display_links = ('id', 'name')
    list_filter = ('name', 'phone', 'email')
    search_fields = ('name', 'phone', 'email', 'contact_date')
    list_per_page = 25

admin.site.register(Contact, ContactAdmin)



