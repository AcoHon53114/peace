from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Register your models here.
from .models import New

class NewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'translation_status', 'list_date')
    list_display_links = ('id', 'title')
    list_filter = ('title',)
    list_editable = ('is_published',)
    search_fields = ('title', 'title_zh_hans', 'title_en', 'description', 'description_zh_hans', 'description_en', 'youtube_link')
    fieldsets = (
        (_('Traditional Chinese content'), {'fields': ('title', 'description'), 'classes': ('content-language-group',)}),
        (_('Simplified Chinese content'), {'fields': ('title_zh_hans', 'description_zh_hans'), 'classes': ('content-language-group',)}),
        (_('English content'), {'fields': ('title_en', 'description_en'), 'classes': ('content-language-group',)}),
        (_('Shared information'), {'fields': ('photo_main', 'photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5', 'photo_6', 'photo_7', 'photo_8', 'photo_9', 'youtube_link', 'is_published')}),
    )

    @admin.display(description=_('Translation status'))
    def translation_status(self, obj):
        labels = []
        for suffix, label in [('', '繁'), ('_zh_hans', '简'), ('_en', 'EN')]:
            complete = bool(getattr(obj, 'title' + suffix).strip()) and (
                not obj.description or bool(getattr(obj, 'description' + suffix).strip()))
            labels.append(label + ': ' + str(_('Complete') if complete else _('Incomplete')))
        return ' / '.join(labels)

    list_per_page = (25)
    
admin.site.register(New, NewAdmin)
