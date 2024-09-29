from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Resident

# Register your models here.

class ResidentResource(resources.ModelResource):

    class Meta:
        model = Resident

class ResidentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'username', 'resident_code', 'resident_name', 'resident_contact_person', 'resident_contact_phone', 'resident_contact_relation')
    list_display_links = ('username', 'resident_code', 'resident_name')
    list_filter = ('username', 'resident_code', 'resident_name')
    search_fields = ('username', 'resident_code', 'resident_name')
    list_per_page = 25
    resource_classes = [ResidentResource]

admin.site.register(Resident, ResidentAdmin)