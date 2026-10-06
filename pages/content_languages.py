"""Select stored content without changing original Traditional Chinese values."""
from django.utils.translation import get_language


def content_suffix():
    return {'en': '_en', 'zh-hans': '_zh_hans'}.get(get_language(), '')


def localized_value(obj, field):
    suffix = content_suffix()
    translated = getattr(obj, field + suffix, '') if suffix else ''
    return translated.strip() or getattr(obj, field)


def translation_incomplete(obj, fields):
    suffix = content_suffix()
    return bool(suffix and any(getattr(obj, field) and not getattr(obj, field + suffix, '').strip()
                               for field in fields))
