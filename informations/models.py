from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from informations.choices import title_choices
from datetime import datetime


# Create your models here.
class Booking(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=20,choices=title_choices.items(),default='預約參觀選位')
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    phone = models.CharField(verbose_name=_('Phone'), max_length=100)
    email = models.CharField(verbose_name=_('Email'), max_length=50)
    #visit_date_time = models.DateTimeField(default=datetime.now, blank=True)
    comment = models.TextField(verbose_name=_('Comment'), blank=True, null=True)
    submit_date = models.DateTimeField(verbose_name=_('Submission date'), default=datetime.now, blank=True)
    visit_date = models.DateField(verbose_name=_('Visit date'), default=timezone.now)  # 新增的日期欄位
    visit_time = models.TimeField(verbose_name=_('Visit time'), default=timezone.now)

    class Meta:
        verbose_name = _('Visit booking')
        verbose_name_plural = _('Visit bookings')

    def __str__(self):
        return f"{self.name} - {self.visit_date} {self.visit_time}"
