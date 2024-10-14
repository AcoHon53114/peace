from django import template
from django.utils.timesince import timesince
from django.utils.translation import gettext as _

register = template.Library()

@register.filter
def timesince_zh(value, arg=None):
    if not value:
        return ''
    if arg:
        return timesince(value, arg)
    result = timesince(value)
    result = result.replace('years', '年').replace('year', '年')
    result = result.replace('weeks', '星期').replace('week', '星期')
    result = result.replace('days', '天').replace('day', '天')
    result = result.replace('hours', '小時').replace('hour', '小時')
    result = result.replace('minutes', '分鐘').replace('minute', '分鐘')
    result = result.replace('seconds', '秒').replace('second', '秒')
    return result