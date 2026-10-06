from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client, TestCase, TransactionTestCase
from django.utils.translation import override
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from news.models import New
from environments.models import Voice


class AdminContentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_superuser('admin-content-test', 'qa@example.com', 'qa-password')
        cls.item = New.objects.create(title='原文消息', description='繁體原文', photo_main='existing.jpg',
                                      title_en='English news', description_en='English content',
                                      title_zh_hans='简体消息', description_zh_hans='简体内容')
        cls.voice = Voice.objects.create(name='蘇姑娘', description='照顧周到', photo='existing-voice.jpg',
                                         name_en='Ms So', description_en='Thoughtful care',
                                         name_zh_hans='苏姑娘', description_zh_hans='照顾周到')

    def test_admin_preference_is_independent(self):
        self.client.cookies[settings.LANGUAGE_COOKIE_NAME] = 'en'
        self.assertEqual(self.client.get('/admin/login/').headers['Content-Language'], 'zh-hant')
        self.assertContains(self.client.get('/admin/login/'), 'id="admin-language-select"')
        response = self.client.post('/admin/set-language/', {'language': 'zh-hans', 'next': '/admin/login/?next=/admin/'})
        self.assertEqual(response.url, '/admin/login/?next=/admin/')
        self.assertEqual(response.cookies['peace_admin_language']['path'], '/admin/')
        self.assertEqual(response.cookies['peace_admin_language'].value, 'zh-hans')
        self.assertTrue(response.cookies['peace_admin_language']['httponly'])
        self.assertNotIn(settings.LANGUAGE_COOKIE_NAME, response.cookies)
        self.assertEqual(self.client.get('/admin/login/').headers['Content-Language'], 'zh-hans')
        self.assertEqual(self.client.get('/').headers['Content-Language'], 'en')

    def test_invalid_language_and_external_redirect(self):
        self.assertEqual(self.client.get('/admin/set-language/').status_code, 405)
        self.assertEqual(self.client.post('/admin/set-language/', {'language': 'xx'}).status_code, 400)
        for target in ('https://evil.example/admin/', '//evil.example/admin/', '/accounts/login'):
            self.assertEqual(self.client.post('/admin/set-language/', {'language': 'en', 'next': target}).url, '/admin/')

    def test_switch_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post('/admin/set-language/', {'language': 'en'}).status_code, 403)
        client.get('/admin/login/')
        token = client.cookies['csrftoken'].value
        self.assertEqual(client.post('/admin/set-language/', {'language': 'en', 'csrfmiddlewaretoken': token}).status_code, 302)

    def test_admin_custom_labels_in_all_languages(self):
        self.client.force_login(self.staff)
        for lang,heading,field in [('zh-hant','繁體中文內容','標題（英文）'),
                                   ('zh-hans','繁体中文内容','标题（英文）'),
                                   ('en','Traditional Chinese content','Title (English)')]:
            self.client.cookies['peace_admin_language'] = lang
            response = self.client.get(f'/admin/news/new/{self.item.pk}/change/')
            self.assertContains(response, heading)
            self.assertContains(response, field)
            self.assertContains(response, 'name="title_en"')
            self.assertContains(response, 'name="title_zh_hans"')
            self.assertContains(response, 'value="原文消息"')

    def test_public_localized_content(self):
        for lang,title,body,name,voice in [('zh-hant','原文消息','繁體原文','蘇姑娘','照顧周到'),
                                         ('zh-hans','简体消息','简体内容','苏姑娘','照顾周到'),
                                         ('en','English news','English content','Ms So','Thoughtful care')]:
            self.client.cookies[settings.LANGUAGE_COOKIE_NAME] = lang
            for path in ('/news/', f'/news/{self.item.pk}'):
                response = self.client.get(path)
                self.assertContains(response, title)
                self.assertContains(response, body)
                self.assertNotContains(response, 'content-translation-note')
            response = self.client.get('/environments/')
            self.assertContains(response, name)
            self.assertContains(response, voice)
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, '原文消息')
        self.assertEqual(self.item.photo_main.name, 'existing.jpg')

    def test_partial_translation_has_field_fallback_and_notice(self):
        self.item.description_en = ''
        self.item.save()
        self.voice.description_zh_hans = ''
        self.voice.save()
        self.client.cookies[settings.LANGUAGE_COOKIE_NAME] = 'en'
        response = self.client.get(f'/news/{self.item.pk}')
        self.assertContains(response, 'English news')
        self.assertContains(response, '繁體原文')
        self.assertContains(response, 'This translation is incomplete')
        self.client.cookies[settings.LANGUAGE_COOKIE_NAME] = 'zh-hans'
        response = self.client.get('/environments/')
        self.assertContains(response, '苏姑娘')
        self.assertContains(response, '照顧周到')
        self.assertContains(response, '此内容的翻译尚未完成')

    def test_search_uses_selected_title_and_displayed_fallback(self):
        self.client.cookies[settings.LANGUAGE_COOKIE_NAME] = 'en'
        response = self.client.get('/news/search', {'title': 'English'})
        self.assertContains(response, 'English news')
        response = self.client.get('/news/search', {'title': '原文消息'})
        self.assertNotContains(response, 'English news')
        self.item.title_en = ''
        self.item.save()
        response = self.client.get('/news/search', {'title': '原文消息'})
        self.assertContains(response, '原文消息')

    def test_admin_search_and_completion_status(self):
        self.client.force_login(self.staff)
        self.client.cookies['peace_admin_language'] = 'en'
        response = self.client.get('/admin/news/new/', {'q': 'English news'})
        self.assertContains(response, '原文消息')
        self.assertContains(response, 'EN: Complete')
        self.item.description_en = ''
        self.item.save()
        self.assertContains(self.client.get('/admin/news/new/'), 'EN: Incomplete')

    def test_saving_translations_preserves_original_and_shared_assets(self):
        self.client.force_login(self.staff)
        response = self.client.post(f'/admin/news/new/{self.item.pk}/change/', {
            'title': self.item.title, 'description': self.item.description,
            'title_en': 'A much longer English title for our activities', 'description_en': 'Updated English content',
            'title_zh_hans': self.item.title_zh_hans, 'description_zh_hans': self.item.description_zh_hans,
            'youtube_link': '', 'is_published': 'on', '_save': 'Save'})
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, '原文消息')
        self.assertEqual(self.item.description, '繁體原文')
        self.assertEqual(self.item.photo_main.name, 'existing.jpg')
        self.assertEqual(self.item.title_en, 'A much longer English title for our activities')


class ContentMigrationTests(TransactionTestCase):
    def test_existing_rows_survive_new_language_columns(self):
        previous = [('news', '0003_alter_new_title_alter_new_youtube_link'), ('environments', '0002_voice_is_published')]
        target = [('news', '0004_alter_new_options_new_description_en_and_more'),
                  ('environments', '0003_alter_voice_options_voice_description_en_and_more')]
        executor = MigrationExecutor(connection)
        executor.migrate(previous)
        old = executor.loader.project_state(previous).apps
        item = old.get_model('news', 'New').objects.create(title='原文保留', description='繁體內容', photo_main='old.jpg', photo_1='old-1.jpg', youtube_link='https://www.youtube.com/watch?v=test')
        original_date = item.list_date
        voice = old.get_model('environments', 'Voice').objects.create(name='原名', description='原心聲', photo='voice.jpg')
        try:
            executor = MigrationExecutor(connection)
            executor.migrate(target)
            item = New.objects.get(pk=item.pk)
            voice = Voice.objects.get(pk=voice.pk)
            self.assertEqual((item.title, item.description, item.photo_main.name), ('原文保留', '繁體內容', 'old.jpg'))
            self.assertEqual(item.list_date, original_date)
            self.assertEqual(item.photo_1.name, 'old-1.jpg')
            self.assertEqual(item.youtube_link, 'https://www.youtube.com/watch?v=test')
            self.assertEqual((voice.name, voice.description, voice.photo.name), ('原名', '原心聲', 'voice.jpg'))
            self.assertEqual((item.title_en, item.title_zh_hans, voice.name_en, voice.name_zh_hans), ('', '', '', ''))
        finally:
            MigrationExecutor(connection).migrate(target)
