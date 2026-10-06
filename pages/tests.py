import re

from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils.translation import gettext, override, to_locale
from banks.models import Bank
from news.models import New
from residents.models import Resident


class LanguageSwitchTests(TestCase):
    def test_chinese_catalogues_use_django_locale_names(self):
        for language in ('zh-hans', 'zh-hant'):
            catalogue = settings.BASE_DIR / 'locale' / to_locale(language) / 'LC_MESSAGES' / 'django.mo'
            self.assertTrue(catalogue.is_file(), str(catalogue))

    def test_actual_chinese_text_changes_with_language(self):
        examples = {
            'zh-hans': ('关于我们', '注册', '院舍环境', '关怀'),
            'zh-hant': ('關於我們', '註冊', '院舍環境', '關懷'),
        }
        for language, expected in examples.items():
            with self.subTest(language=language):
                self.client.cookies[settings.LANGUAGE_COOKIE_NAME] = language
                response = self.client.get('/')
                for text in expected:
                    self.assertContains(response, text)
                opposite = examples['zh-hant' if language == 'zh-hans' else 'zh-hans']
                rendered = re.sub(r'<!--[\s\S]*?-->', '', response.content.decode())
                for text in opposite:
                    self.assertNotIn(text, rendered)
                with override(language):
                    self.assertEqual(gettext('關於我們'), expected[0])
                    self.assertEqual(gettext('註冊'), expected[1])
                response = self.client.post('/informations/', {'name': '', 'email': 'bad', 'phone': '1'})
                self.assertContains(response, '姓名是必填的。')
                self.assertContains(response, '请输入有效的8位电话号码。' if language == 'zh-hans'
                                    else '請輸入有效的8位電話號碼。')

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('language-test', password='test-password')
        resident = Resident.objects.create(username=cls.user, resident_code='QA001', resident_name='原文姓名')
        Bank.objects.create(user_id=cls.user.id, resident_id=resident.id,
                            resident_code='QA001', resident_name='原文姓名',
                            payment_method='銀行轉帳', payment_month='1月份',
                            payment_year='2026', depositslip_photo='test.pdf')
        New.objects.create(pk=1, title='原文消息', description='保持原文', photo_main='test.jpg')

    def test_all_languages_render_public_pages(self):
        paths = ['/', '/about', '/environments/', '/news/', '/news/1',
                 '/informations/', '/informations/guideline', '/contacts/',
                 '/accounts/login', '/accounts/register']
        for language in dict(settings.LANGUAGES):
            self.client.cookies[settings.LANGUAGE_COOKIE_NAME] = language
            for path in paths:
                with self.subTest(language=language, path=path):
                    response = self.client.get(path)
                    self.assertEqual(response.status_code, 200)
                    self.assertContains(response, f'<html lang="{language}">')
                    self.assertEqual(response.headers['Content-Language'], language)

    def test_default_is_traditional_chinese_and_admin_stays_english(self):
        client = Client(HTTP_ACCEPT_LANGUAGE='en')
        self.assertEqual(client.get('/').headers['Content-Language'], 'zh-hant')
        client.cookies[settings.LANGUAGE_COOKIE_NAME] = 'zh-hans'
        self.assertEqual(client.get('/admin/login/').headers['Content-Language'], 'en-us')

    def test_switch_preserves_location_and_rejects_external_redirect(self):
        response = self.client.post('/i18n/setlang/', {
            'language': 'en', 'next': '/about?source=test#booking-section'})
        self.assertEqual(response.url, '/about?source=test#booking-section')
        self.assertEqual(response.cookies[settings.LANGUAGE_COOKIE_NAME].value, 'en')
        response = self.client.post('/i18n/setlang/', {'language': 'en', 'next': 'https://evil.example/'})
        self.assertNotIn('evil.example', response.url)

    def test_switch_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post('/i18n/setlang/', {'language': 'en'}).status_code, 403)
        client.get('/')
        token = client.cookies['csrftoken'].value
        self.assertEqual(client.post('/i18n/setlang/', {
            'language': 'en', 'csrfmiddlewaretoken': token}).status_code, 302)

    def test_english_choices_preserve_stored_values_and_dynamic_content(self):
        self.client.cookies[settings.LANGUAGE_COOKIE_NAME] = 'en'
        self.client.force_login(self.user)
        response = self.client.get('/accounts/dashboard')
        for text in ['Bank Transfer', 'January', 'value="銀行轉帳"',
                     'value="1月份"', '原文姓名', 'View Record']:
            self.assertContains(response, text)
        response = self.client.get('/news/1')
        self.assertContains(response, '原文消息')
        self.assertContains(response, '保持原文')
        self.assertContains(response, 'Back to News')
        response = self.client.get('/informations/')
        self.assertContains(response, 'value="Mr"')
        self.assertContains(response, '>Mr</option>')

    def test_existing_booking_errors_are_translated(self):
        self.client.cookies[settings.LANGUAGE_COOKIE_NAME] = 'en'
        response = self.client.post('/informations/', {'name': '', 'email': 'bad', 'phone': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Name is required.')
        self.assertContains(response, 'Please enter a valid 8-digit phone number.')
