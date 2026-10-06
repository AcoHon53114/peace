from urllib.parse import urlencode
from django import template
from django.utils import formats, timezone, translation

register = template.Library()

@register.filter
def ui_date(value):
    return formats.date_format(value, 'DATE_FORMAT' if translation.get_language() == 'en' else 'Y年m月d日') if value else ''

@register.filter
def ui_datetime(value):
    if not value:
        return ''
    if timezone.is_aware(value):
        value = timezone.localtime(value)
    return formats.date_format(value, 'DATETIME_FORMAT' if translation.get_language() == 'en' else 'Y年m月d日 H:i')

@register.simple_tag
def whatsapp_link():
    message = translation.gettext('我想了解更多平安護老院的服務及資訊')
    return 'https://api.whatsapp.com/send?' + urlencode({'phone': '85256466945', 'text': message})
