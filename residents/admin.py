from django.contrib import admin
from .models import Resident
# Register your models here.


class ResidentAdmin(admin.ModelAdmin):
    list_display = ('username', 'resident_id', 'resident_name', 'resident_contact_person', 'resident_contact_phone',
'resident_contact_relation')
    list_display_links = ('username', 'resident_id', 'resident_name')
    list_filter = ('username', 'resident_id', 'resident_name')
    search_fields = ('username', 'resident_id', 'resident_name')
    list_per_page = (25)
    
admin.site.register(Resident, ResidentAdmin)
