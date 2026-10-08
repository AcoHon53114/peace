"""Pages notifications: use only test DB and mocked GitHub, never real credentials."""
import json
from io import BytesIO
from unittest.mock import Mock, MagicMock, patch
from urllib.error import HTTPError
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction, connection
from django.test import TestCase, TransactionTestCase, RequestFactory, override_settings
from django.utils.translation import override
from PIL import Image
from news.models import New
from environments.models import Voice
from peaceweb.pages_sync import dispatch_pages_workflow, schedule_pages_sync

CONFIG = dict(PEACE_PAGES_SYNC_ENABLED=True, PEACE_PAGES_DEPLOYMENT_ENV='production',
              PEACE_PAGES_GITHUB_TOKEN='mock-token-not-a-credential',
              PEACE_PAGES_GITHUB_REPOSITORY='AcoHon53114/peace',
              PEACE_PAGES_GITHUB_WORKFLOW='pages-demo.yml', PEACE_PAGES_GITHUB_REF='main')


def photo():
    stream = BytesIO()
    Image.new('RGB', (2, 2), 'white').save(stream, 'PNG')
    return SimpleUploadedFile('test.png', stream.getvalue(), content_type='image/png')


@override_settings(**CONFIG)
class AdminPagesSyncTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_superuser('sync-staff', 'qa@example.com', 'qa-password')
        cls.item = New.objects.create(title='公開消息', description='原文', photo_main='existing.jpg')
        cls.draft = New.objects.create(title='草稿', description='草稿內容', photo_main='draft.jpg', is_published=False)
        cls.voice = Voice.objects.create(name='蘇姑娘', description='照顧周到', photo='voice.jpg')

    def setUp(self):
        self.client.force_login(self.staff)
        self.client.cookies['peace_admin_language'] = 'en'
        self.patcher = patch('peaceweb.pages_sync.dispatch_pages_workflow', return_value=True)
        self.dispatch = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def data(self, obj, **changes):
        if isinstance(obj, New):
            fields = ('title', 'description', 'title_en', 'title_zh_hans', 'description_en', 'description_zh_hans', 'youtube_link')
        else:
            fields = ('name', 'description', 'name_en', 'name_zh_hans', 'description_en', 'description_zh_hans')
        values = {name: getattr(obj, name) for name in fields}
        if obj.is_published: values['is_published'] = 'on'
        values['_save'] = 'Save'
        values.update(changes)
        return values

    def save(self, obj, **changes):
        path = f'/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/change/'
        with self.captureOnCommitCallbacks(execute=True) as callbacks:
            response = self.client.post(path, self.data(obj, **changes))
            self.dispatch.assert_not_called()
        return response, callbacks

    def test_public_news_edit_notifies_after_commit(self):
        response, callbacks = self.save(self.item, title_en='Updated English news')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(callbacks), 1)
        self.dispatch.assert_called_once_with()
        self.item.refresh_from_db()
        self.assertEqual(self.item.title_en, 'Updated English news')

    def test_public_voice_edit_notifies(self):
        response, _ = self.save(self.voice, description_zh_hans='新的简体内容')
        self.assertEqual(response.status_code, 302)
        self.dispatch.assert_called_once()

    def test_draft_edit_does_not_notify(self):
        response, callbacks = self.save(self.draft, description='草稿更新')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(callbacks, [])
        self.dispatch.assert_not_called()

    def test_publish_draft_notifies(self):
        response, _ = self.save(self.draft, is_published='on')
        self.assertEqual(response.status_code, 302)
        self.dispatch.assert_called_once()

    def test_unpublish_notifies(self):
        response, _ = self.save(self.item, is_published='')
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertFalse(self.item.is_published)
        self.dispatch.assert_called_once()

    def test_unchanged_save_does_not_notify(self):
        response, callbacks = self.save(self.item)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(callbacks, [])
        self.dispatch.assert_not_called()

    def test_invalid_form_does_not_notify(self):
        response, callbacks = self.save(self.item, title='')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(callbacks, [])
        self.dispatch.assert_not_called()

    @override_settings(PEACE_PAGES_DEPLOYMENT_ENV='preview')
    def test_preview_saves_without_notification(self):
        response, callbacks = self.save(self.item, description='預覽更新')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(callbacks, [])
        self.dispatch.assert_not_called()

    @override_settings(PEACE_PAGES_DEPLOYMENT_ENV='')
    def test_local_saves_without_notification(self):
        response, callbacks = self.save(self.item, description='本機更新')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(callbacks, [])

    @override_settings(PEACE_PAGES_SYNC_ENABLED=False)
    def test_disabled_saves_without_notification(self):
        response, callbacks = self.save(self.item, description='未啟用通知')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(callbacks, [])

    def test_notification_failure_preserves_save_and_warns(self):
        self.dispatch.return_value = False
        response, _ = self.save(self.item, description='已儲存新內容')
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.description, '已儲存新內容')
        self.dispatch.assert_called_once()

    def test_unexpected_notification_exception_preserves_save(self):
        self.dispatch.side_effect = RuntimeError('test exception')
        with self.assertLogs('peaceweb.pages_sync', level='WARNING'):
            response, _ = self.save(self.item, description='保留已儲存內容')
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.description, '保留已儲存內容')

    def test_success_message_in_all_three_admin_languages(self):
        for language, text in [('zh-hant', '已提出展示網站同步要求'), ('zh-hans', '已提出展示网站同步请求'),
                               ('en', 'A demo website sync has been requested')]:
            self.dispatch.reset_mock()
            self.client.cookies['peace_admin_language'] = language
            self.item.refresh_from_db()
            with override(language), patch.object(admin.site._registry[New], 'message_user') as message:
                response, _ = self.save(self.item, description=language)
            self.assertIn(text, str(message.call_args.args[1]))

    def test_failure_message_in_all_three_admin_languages(self):
        self.dispatch.return_value = False
        for language, text in [('zh-hant', '即時展示網站同步通知失敗'), ('zh-hans', '即时展示网站同步通知失败'),
                               ('en', 'immediate demo sync notification failed')]:
            self.dispatch.reset_mock()
            self.client.cookies['peace_admin_language'] = language
            self.item.refresh_from_db()
            with override(language), patch.object(admin.site._registry[New], 'message_user') as message:
                response, _ = self.save(self.item, description=language)
            self.assertIn(text, str(message.call_args.args[1]))

    def test_single_public_delete_notifies(self):
        with self.captureOnCommitCallbacks(execute=True) as callbacks:
            response = self.client.post(f'/admin/news/new/{self.item.pk}/delete/', {'post': 'yes'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(New.objects.filter(pk=self.item.pk).exists())
        self.assertEqual(len(callbacks), 1)
        self.dispatch.assert_called_once()

    def test_single_draft_delete_does_not_notify(self):
        with self.captureOnCommitCallbacks(execute=True) as callbacks:
            response = self.client.post(f'/admin/news/new/{self.draft.pk}/delete/', {'post': 'yes'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(callbacks, [])
        self.dispatch.assert_not_called()

    def test_public_voice_delete_notifies(self):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(f'/admin/environments/voice/{self.voice.pk}/delete/', {'post': 'yes'})
        self.assertEqual(response.status_code, 302)
        self.dispatch.assert_called_once()

    def test_bulk_delete_notifies_once(self):
        other = New.objects.create(title='另一消息', photo_main='other.jpg')
        with self.captureOnCommitCallbacks(execute=True) as callbacks:
            response = self.client.post('/admin/news/new/', {'action': 'delete_selected', 'post': 'yes',
                '_selected_action': [str(self.item.pk), str(self.draft.pk), str(other.pk)]})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(New.objects.count(), 0)
        self.assertEqual(len(callbacks), 1)
        self.dispatch.assert_called_once()

    def test_bulk_draft_delete_does_not_notify(self):
        with self.captureOnCommitCallbacks(execute=True) as callbacks:
            response = self.client.post('/admin/news/new/', {'action': 'delete_selected', 'post': 'yes',
                '_selected_action': [str(self.draft.pk)]})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(callbacks, [])
        self.dispatch.assert_not_called()

    def test_list_editable_multiple_changes_notifies_once(self):
        with self.captureOnCommitCallbacks(execute=True) as callbacks:
            response = self.client.post('/admin/news/new/', {'_save': 'Save', 'form-TOTAL_FORMS': '2',
                'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000',
                'form-0-id': str(self.draft.pk), 'form-0-is_published': 'on',
                'form-1-id': str(self.item.pk)})
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db(); self.draft.refresh_from_db()
        self.assertFalse(self.item.is_published); self.assertTrue(self.draft.is_published)
        self.assertEqual(len(callbacks), 1)
        self.dispatch.assert_called_once()

    def test_draft_voice_edit_does_not_notify(self):
        self.voice.is_published = False; self.voice.save()
        response, callbacks = self.save(self.voice, description='草稿心聲')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(callbacks, [])

    def test_new_published_and_draft_items(self):
        import tempfile
        with tempfile.TemporaryDirectory() as media, override_settings(MEDIA_ROOT=media):
            for public in (True, False):
                self.dispatch.reset_mock()
                data = {'title': '新消息', 'description': '新內容', 'photo_main': photo(), '_save': 'Save'}
                if public: data['is_published'] = 'on'
                with self.captureOnCommitCallbacks(execute=True) as callbacks:
                    response = self.client.post('/admin/news/new/add/', data)
                self.assertEqual(response.status_code, 302)
                self.assertEqual(len(callbacks), int(public))
                self.assertEqual(self.dispatch.call_count, int(public))

    def test_changed_photo_notifies(self):
        import tempfile
        with tempfile.TemporaryDirectory() as media, override_settings(MEDIA_ROOT=media):
            response, _ = self.save(self.item, photo_main=photo())
        self.assertEqual(response.status_code, 302)
        self.dispatch.assert_called_once()

    def test_other_admin_model_does_not_notify(self):
        with self.captureOnCommitCallbacks(execute=True) as callbacks:
            response = self.client.post('/admin/auth/group/add/', {'name': 'Internal group', '_save': 'Save'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(callbacks, [])
        self.dispatch.assert_not_called()


@override_settings(**CONFIG)
class CommitTests(TransactionTestCase):
    def test_real_admin_response_persists_success_and_failure_messages(self):
        user = User.objects.create_superuser('commit-staff', 'qa@example.com', 'qa-password')
        self.client.force_login(user)
        item = New.objects.create(title='真實提交', description='原文', photo_main='test.jpg')
        for accepted in (True, False):
            for language, success, failure in [
                ('zh-hant', '已提出展示網站同步要求', '即時展示網站同步通知失敗'),
                ('zh-hans', '已提出展示网站同步请求', '即时展示网站同步通知失败'),
                ('en', 'A demo website sync has been requested', 'immediate demo sync notification failed')]:
                self.client.cookies['peace_admin_language'] = language
                with patch('peaceweb.pages_sync.dispatch_pages_workflow', return_value=accepted) as dispatch:
                    response = self.client.post(f'/admin/news/new/{item.pk}/change/', {
                        'title': item.title, 'description': language + str(accepted), 'is_published': 'on', '_save': 'Save'})
                self.assertEqual(response.status_code, 302)
                dispatch.assert_called_once()
                self.assertContains(self.client.get(response.url), success if accepted else failure)

    def test_real_commit_happens_before_notification(self):
        request = RequestFactory().post('/admin/news/new/add/')
        model_admin = admin.site._registry[New]
        form = Mock(); form.has_changed.return_value = True
        item = New(title='提交測試', photo_main='test.jpg')
        def accepted():
            self.assertFalse(connection.in_atomic_block)
            self.assertTrue(New.objects.filter(pk=item.pk).exists())
            return True
        with patch('peaceweb.pages_sync.dispatch_pages_workflow', side_effect=accepted) as dispatch, \
                patch.object(model_admin, 'message_user'):
            with transaction.atomic():
                model_admin.save_model(request, item, form, False)
                dispatch.assert_not_called()
            dispatch.assert_called_once()

    def test_real_rollback_discards_notification(self):
        request = RequestFactory().post('/admin/news/new/add/')
        model_admin = admin.site._registry[New]
        item = New(title='回滾測試', photo_main='test.jpg')
        form = Mock(); form.has_changed.return_value = True
        with patch('peaceweb.pages_sync.dispatch_pages_workflow') as dispatch:
            with self.assertRaises(RuntimeError):
                with transaction.atomic():
                    model_admin.save_model(request, item, form, False)
                    raise RuntimeError('later related save failed')
            self.assertFalse(New.objects.filter(pk=item.pk).exists())
            dispatch.assert_not_called()


@override_settings(**CONFIG)
class GitHubTransportTests(TestCase):
    def opener(self, status=204):
        mock = MagicMock()
        response = mock.open.return_value.__enter__.return_value
        response.status = status
        return mock

    def test_exact_workflow_request_contains_no_content(self):
        opener = self.opener()
        with patch('peaceweb.pages_sync.build_opener', return_value=opener):
            self.assertTrue(dispatch_pages_workflow())
        request = opener.open.call_args.args[0]
        self.assertEqual(request.full_url, 'https://api.github.com/repos/AcoHon53114/peace/actions/workflows/pages-demo.yml/dispatches')
        self.assertEqual(request.method, 'POST')
        self.assertEqual(json.loads(request.data), {'ref': 'main'})
        self.assertEqual(opener.open.call_args.kwargs['timeout'], 4)
        self.assertEqual(request.get_header('Authorization'), 'Bearer mock-token-not-a-credential')

    def test_current_and_legacy_acceptance_statuses(self):
        for status in (200, 204):
            with patch('peaceweb.pages_sync.build_opener', return_value=self.opener(status)):
                self.assertTrue(dispatch_pages_workflow())

    def test_http_failure_is_contained_without_response_body(self):
        opener = self.opener()
        opener.open.side_effect = HTTPError('https://api.github.com/', 403, 'mock-token-not-a-credential', {}, None)
        with patch('peaceweb.pages_sync.build_opener', return_value=opener), self.assertLogs('peaceweb.pages_sync', level='WARNING') as logs:
            self.assertFalse(dispatch_pages_workflow())
        self.assertNotIn('mock-token-not-a-credential', '\n'.join(logs.output))

    def test_timeout_is_contained_without_exception_text(self):
        opener = self.opener()
        opener.open.side_effect = TimeoutError('mock-token-not-a-credential')
        with patch('peaceweb.pages_sync.build_opener', return_value=opener), self.assertLogs('peaceweb.pages_sync', level='WARNING') as logs:
            self.assertFalse(dispatch_pages_workflow())
        self.assertNotIn('mock-token-not-a-credential', '\n'.join(logs.output))

    @override_settings(PEACE_PAGES_GITHUB_TOKEN='')
    def test_missing_token_does_not_send_request(self):
        with patch('peaceweb.pages_sync.build_opener') as opener, self.assertLogs('peaceweb.pages_sync', level='WARNING'):
            self.assertFalse(dispatch_pages_workflow())
        opener.assert_not_called()

    @override_settings(PEACE_PAGES_GITHUB_REPOSITORY='evil.example/path/injection')
    def test_invalid_configuration_does_not_send_request(self):
        with patch('peaceweb.pages_sync.build_opener') as opener, self.assertLogs('peaceweb.pages_sync', level='WARNING'):
            self.assertFalse(dispatch_pages_workflow())
        opener.assert_not_called()

    def test_redirects_are_not_followed(self):
        from peaceweb.pages_sync import _NoRedirect
        self.assertIsNone(_NoRedirect().redirect_request(None, None, 302, 'redirect', {}, 'https://evil.example/'))
