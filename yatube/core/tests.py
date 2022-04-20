from django.test import TestCase, Client


class ViewTestClass(TestCase):
    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest_client = Client()

    def test_error_page(self):
        'Проверка страницы 404'
        response = self.client.get('/nonexist-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'core/404.html',
                                'Шаблон 404 не соответствует'
                                )
