from django.conf import settings
from django.middleware.locale import LocaleMiddleware
from django.utils import translation


class SiteLocaleMiddleware(LocaleMiddleware):
    """Traditional Chinese until explicitly selected; admin has an independent language preference."""
    def process_request(self, request):
        if request.path_info.startswith('/admin/'):
            selected = request.COOKIES.get('peace_admin_language')
            language = selected if selected in dict(settings.LANGUAGES) else settings.LANGUAGE_CODE
        else:
            selected = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
            language = selected if selected in dict(settings.LANGUAGES) else settings.LANGUAGE_CODE
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()
