from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from http import HTTPStatus
from django.urls import reverse


User = get_user_model()


class PostURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.urls = {
            'author': reverse('about:author'),
            'tech': reverse('about:tech'),
        }

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()

    def test_author(self):
        'Проверка страницы автор'
        response = self.guest_client.get(self.urls['author'])
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'ОШИБКА: Cтраница автор работает не верно!')

    def test_tech(self):
        'Проверка страниц технологий'
        response = self.guest_client.get(self.urls['tech'])
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'ОШИБКА: страница технологий работает не верно!')

    def test_urls_uses_correct_template(self):
        'URL-адрес использует соответствующий шаблон'
        # Шаблоны по адресам
        templates_url_names = {
            self.urls['author']: 'about/author.html',
            self.urls['tech']: 'about/tech.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)
