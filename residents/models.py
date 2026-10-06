from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class Resident(models.Model):
    username = models.OneToOneField(User, verbose_name=_('User account'), on_delete=models.DO_NOTHING)
    resident_name = models.CharField(verbose_name=_('Resident name'), max_length=50)
    resident_code = models.CharField(verbose_name=_('Resident code'), max_length=50, unique=True)
    resident_description = models.CharField(verbose_name=_('Resident description'), max_length=200)
    resident_contact_person = models.CharField(verbose_name=_('Contact person'), max_length=80)
    resident_contact_phone = models.CharField(verbose_name=_('Contact phone'), max_length=100)
    resident_contact_email = models.CharField(verbose_name=_('Contact email'), max_length=100)
    resident_contact_relation = models.CharField(verbose_name=_('Relationship'), max_length=100)

    class Meta:
        verbose_name = _('Resident')
        verbose_name_plural = _('Residents')

    def __str__(self):
        return self.resident_name
