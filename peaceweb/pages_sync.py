"""Notify the existing Pages workflow after a public Admin change commits.

No background threads, database schema changes, or content/credentials in the
dispatch payload. The hourly Pages check remains the fallback on failure.
"""
import json
import logging
import re
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import HTTPRedirectHandler, Request, build_opener

from django.conf import settings
from django.contrib import messages
from django.db import router, transaction
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Do not forward the GitHub Authorization header to a redirect target.
        return None


def dispatch_pages_workflow():
    """Return whether GitHub accepted the request; never log tokens or bodies."""
    token = settings.PEACE_PAGES_GITHUB_TOKEN
    repository = settings.PEACE_PAGES_GITHUB_REPOSITORY
    workflow = settings.PEACE_PAGES_GITHUB_WORKFLOW
    ref = settings.PEACE_PAGES_GITHUB_REF
    if (not token or any(char in token for char in '\r\n')
            or not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository)
            or not re.fullmatch(r'[A-Za-z0-9_.-]+\.ya?ml', workflow)
            or not ref):
        logger.warning('Pages sync notification configuration is incomplete or invalid.')
        return False
    url = f'https://api.github.com/repos/{repository}/actions/workflows/{quote(workflow, safe="")}/dispatches'
    try:
        request = Request(url, data=json.dumps({'ref': ref}).encode('utf-8'), method='POST', headers={
            'Authorization': 'Bearer ' + token,
            'Accept': 'application/vnd.github+json',
            'Content-Type': 'application/json',
            'X-GitHub-Api-Version': '2026-03-10',
            'User-Agent': 'Peace-Admin-Pages-Sync/1.0',
        })
        with build_opener(_NoRedirect).open(request, timeout=4) as response:
            accepted = response.status in (200, 204)
        if accepted:
            logger.info('GitHub accepted the Pages sync notification.')
        else:
            logger.warning('GitHub did not accept the Pages sync notification.')
        return accepted
    except HTTPError as exc:
        logger.warning('Pages sync notification failed (GitHub HTTP %s).', exc.code)
        return False
    except Exception:
        # Exception text can include request headers, tokens or response bodies.
        logger.warning('Pages sync notification failed; the hourly check remains available.')
        return False


def _notifications_enabled():
    return settings.PEACE_PAGES_SYNC_ENABLED and settings.PEACE_PAGES_DEPLOYMENT_ENV == 'production'


def schedule_pages_sync(model_admin, request, using):
    if not _notifications_enabled():
        return
    # Admin list_editable and bulk operations can update several rows in one
    # transaction. Register one notification per request/database connection.
    pending = getattr(request, '_peace_pages_sync_pending', None)
    if pending is None:
        pending = request._peace_pages_sync_pending = set()
    if using in pending:
        return
    pending.add(using)

    def after_commit():
        try:
            accepted = dispatch_pages_workflow()
        except Exception:
            logger.warning('Pages sync notification could not complete; saved content is unaffected.')
            accepted = False
        text = (_('Content saved. A demo website sync has been requested; publication may take a few minutes.')
                if accepted else
                _('Content saved, but the immediate demo sync notification failed. The hourly check or Run workflow can retry.'))
        try:
            model_admin.message_user(request, text, level=messages.INFO if accepted else messages.WARNING)
        except Exception:
            # Message rendering must not turn an already committed save into 500.
            logger.warning('Pages sync notification status could not be displayed in Admin.')

    transaction.on_commit(after_commit, using=using, robust=True)


class PublicContentPagesSyncMixin:
    """Admin-only hooks for New and Voice; other business models are untouched."""

    def save_model(self, request, obj, form, change):
        using = router.db_for_write(type(obj), instance=obj)
        should_check = _notifications_enabled() and (not change or form.has_changed())
        was_public = bool(should_check and change and type(obj)._default_manager.using(using).filter(
            pk=obj.pk, is_published=True).exists())
        super().save_model(request, obj, form, change)
        if should_check and (was_public or obj.is_published):
            schedule_pages_sync(self, request, using)

    def delete_model(self, request, obj):
        using = router.db_for_write(type(obj), instance=obj)
        was_public = obj.is_published
        with transaction.atomic(using=using):
            super().delete_model(request, obj)
            if was_public:
                schedule_pages_sync(self, request, using)

    def delete_queryset(self, request, queryset):
        using = queryset.db
        with transaction.atomic(using=using):
            had_public = _notifications_enabled() and queryset.filter(is_published=True).exists()
            super().delete_queryset(request, queryset)
            if had_public:
                schedule_pages_sync(self, request, using)
