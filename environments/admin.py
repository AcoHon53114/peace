from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Register your models here.
from .models import Voice

class VoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'is_published', 'translation_status')
    list_display_links = ('id', 'name')
    list_editable = ('is_published',)
    list_filter = ('name', 'description')
    search_fields = ('name', 'name_zh_hans', 'name_en', 'description', 'description_zh_hans', 'description_en')
    fieldsets = (
        (_('Traditional Chinese content'), {'fields': ('name', 'description'), 'classes': ('content-language-group',)}),
        (_('Simplified Chinese content'), {'fields': ('name_zh_hans', 'description_zh_hans'), 'classes': ('content-language-group',)}),
        (_('English content'), {'fields': ('name_en', 'description_en'), 'classes': ('content-language-group',)}),
        (_('Shared information'), {'fields': ('photo', 'is_published')}),
    )

    @admin.display(description=_('Translation status'))
    def translation_status(self, obj):
        labels = []
        for suffix, label in [('', '繁'), ('_zh_hans', '简'), ('_en', 'EN')]:
            complete = bool(getattr(obj, 'name' + suffix).strip()) and (
                not obj.description or bool(getattr(obj, 'description' + suffix).strip()))
            labels.append(label + ': ' + str(_('Complete') if complete else _('Incomplete')))
        return ' / '.join(labels)

    list_per_page = (25)
    
admin.site.register(Voice, VoiceAdmin)

