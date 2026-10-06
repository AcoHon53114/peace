from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EnvironmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'environments'
    verbose_name = _('Resident testimonials')
