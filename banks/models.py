from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from residents.models import Resident
from django.contrib.auth.models import User
from banks.choices import payment_method_choices, payment_month_choices, payment_year_choices

def current_year():
    return str(datetime.now().year)

def current_month():
    month_number = datetime.now().month
    for key, value in payment_month_choices.items():
        if value.startswith(str(month_number)):
            return key
    return ''

class Bank(models.Model):
    user_id = models.IntegerField(verbose_name=_('User ID'), blank=True)
    resident_id = models.IntegerField(verbose_name=_('Resident ID'), )
    resident_name = models.CharField(verbose_name=_('Resident name'), max_length=200)
    resident_code = models.CharField(verbose_name=_('Resident code'), max_length=200)
    payment_method = models.CharField(verbose_name=_('Payment method'), max_length=20, choices=payment_method_choices.items())
    payment_month = models.CharField(verbose_name=_('Payment month'), max_length=20, choices=payment_month_choices.items(), default=current_month)
    payment_year = models.CharField(verbose_name=_('Payment year'), max_length=20, choices=payment_year_choices.items(), default=current_year)
    depositslip_photo = models.FileField(verbose_name=_('Payment receipt'), upload_to='photos/%Y/%m/%d/')
    comment = models.TextField(verbose_name=_('Comment'), max_length=50)
    uploaded_date = models.DateTimeField(verbose_name=_('Upload date'), default=datetime.now, blank=True)

    class Meta:
        verbose_name = _('Payment record')
        verbose_name_plural = _('Payment records')

    def __str__(self):
        return str(self.resident_name)
