from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime

# Create your models here.
class Contact(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=200)
    email = models.CharField(verbose_name=_('Email'), max_length=100)
    phone = models.CharField(verbose_name=_('Phone'), max_length=80)
    comment = models.TextField(verbose_name=_('Comment'), blank=True)
    contact_date = models.DateTimeField(verbose_name=_('Enquiry date'), default=datetime.now, blank=True)

    class Meta:
        verbose_name = _('Contact enquiry')
        verbose_name_plural = _('Contact enquiries')

    def __str__(self):
        return self.name
