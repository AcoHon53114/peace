from django.db import models
from django.utils.translation import gettext_lazy as _
from pages.content_languages import localized_value, translation_incomplete
from datetime import datetime

# Create your models here.
class New(models.Model):
    title = models.CharField(verbose_name=_('Title (Traditional Chinese)'), max_length=14)
    description = models.TextField(verbose_name=_('Content (Traditional Chinese)'), blank=True)
    is_published = models.BooleanField(verbose_name=_('Published'), default=True)
    youtube_link = models.URLField(verbose_name=_('YouTube URL'), max_length=1000, blank=True)
    list_date = models.DateTimeField(verbose_name=_('Publication date'), auto_now_add=True)
    photo_main = models.ImageField(verbose_name=_('Main photo'), upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(verbose_name=_('Photo 1'), upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(verbose_name=_('Photo 2'), upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(verbose_name=_('Photo 3'), upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(verbose_name=_('Photo 4'), upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(verbose_name=_('Photo 5'), upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(verbose_name=_('Photo 6'), upload_to='photos/%Y/%m/%d/', blank=True)
    photo_7 = models.ImageField(verbose_name=_('Photo 7'), upload_to='photos/%Y/%m/%d/', blank=True)
    photo_8 = models.ImageField(verbose_name=_('Photo 8'), upload_to='photos/%Y/%m/%d/', blank=True)
    photo_9 = models.ImageField(verbose_name=_('Photo 9'), upload_to='photos/%Y/%m/%d/', blank=True)

    title_zh_hans = models.CharField(_('Title (Simplified Chinese)'), max_length=200, blank=True, default='')
    title_en = models.CharField(_('Title (English)'), max_length=200, blank=True, default='')
    description_zh_hans = models.TextField(_('Content (Simplified Chinese)'), blank=True, default='')
    description_en = models.TextField(_('Content (English)'), blank=True, default='')

    @property
    def localized_title(self):
        return localized_value(self, 'title')

    @property
    def localized_description(self):
        return localized_value(self, 'description')

    @property
    def translation_incomplete(self):
        return translation_incomplete(self, ('title', 'description'))

    class Meta:
        verbose_name = _('News item')
        verbose_name_plural = _('News')

    def __str__(self):
        return self.title





