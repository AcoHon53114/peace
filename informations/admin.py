from django.contrib import admin

# Register your models here.
from .models import Voice

class VoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')
    list_filter = ('name', 'description')
    search_fields = ('name', 'description')
    list_per_page = (25)
    
admin.site.register(Voice, VoiceAdmin)
