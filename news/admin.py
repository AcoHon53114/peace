from django.contrib import admin

# Register your models here.
from .models import New

class NewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'list_date')
    list_display_links = ('id', 'title')
    list_filter = ('title',)
    list_editable = ('is_published',)
    search_fields = ('title', 'description', 'youtube_link')
    list_per_page = (25)
    
admin.site.register(New, NewAdmin)
