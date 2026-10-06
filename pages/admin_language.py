from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST


@require_POST
@csrf_protect
def set_admin_language(request):
    language = request.POST.get('language')
    if language not in dict(settings.LANGUAGES):
        return HttpResponseBadRequest('Invalid language')
    target = request.POST.get('next', '/admin/')
    if (not target.startswith('/admin/') or not url_has_allowed_host_and_scheme(
            target, allowed_hosts={request.get_host()}, require_https=request.is_secure())):
        target = '/admin/'
    response = HttpResponseRedirect(target)
    response.set_cookie('peace_admin_language', language,
                        max_age=settings.LANGUAGE_COOKIE_AGE, path='/admin/',
                        secure=settings.LANGUAGE_COOKIE_SECURE,
                        httponly=True, samesite=settings.LANGUAGE_COOKIE_SAMESITE)
    return response
