from django.db import models
from django.utils.translation import gettext_lazy as _
from pages.content_languages import localized_value, translation_incomplete
from datetime import datetime
# Create your models here.

class Voice(models.Model):
    name = models.TextField(verbose_name=_('Name (Traditional Chinese)'), max_length=30)
    photo= models.ImageField(verbose_name=_('Photo'), upload_to='photos/%Y/%m/%d/')
    description = models.TextField(verbose_name=_('Content (Traditional Chinese)'), max_length=50)
    is_published = models.BooleanField(verbose_name=_('Published'), default=True)

    name_zh_hans = models.CharField(_('Name (Simplified Chinese)'), max_length=200, blank=True, default='')
    name_en = models.CharField(_('Name (English)'), max_length=200, blank=True, default='')
    description_zh_hans = models.TextField(_('Content (Simplified Chinese)'), blank=True, default='')
    description_en = models.TextField(_('Content (English)'), blank=True, default='')

    @property
    def localized_name(self):
        return localized_value(self, 'name')

    @property
    def localized_description(self):
        return localized_value(self, 'description')

    @property
    def translation_incomplete(self):
        return translation_incomplete(self, ('name', 'description'))

    class Meta:
        verbose_name = _('Resident testimonial')
        verbose_name_plural = _('Resident testimonials')

    def __str__(self):
        return self.name



