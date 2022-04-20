from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from http import HTTPStatus


User = get_user_model()


class PostURLTests(TestCase):

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя 1
        self.user = User.objects.create_user(username='TestName')
        # Создаем клиент для авторизации
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_signup(self):
        'Проверка страницы регистрации для гостей'
        response = self.guest_client.get('/auth/signup/')
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'ОШИБКА: Регистрация работает не верно!')

    def test_logout_autorization(self):
        'Проверка страницы logout для авторизированных'
        response = self.authorized_client.get('/auth/logout/')
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'ОШИБКА: logout работает не верно!')

    def test_logout_gost(self):
        'Проверка страницы logout для гостей'
        response = self.authorized_client.get('/auth/logout/')
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'ОШИБКА: logout не работает у гостей!')

    def test_login_gost(self):
        'Проверка страниы логина для гостей'
        response = self.guest_client.get('/auth/login/')
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'ОШИБКА: страница логина работает не верно!')
    
    def test_login_autorization(self):
        'Проверка страниы логина для авторизированных'
        response = self.authorized_client.get('/auth/login/')
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'ОШИБКА: страница логина не работает!')

    def test_password_change_gost(self):
        'Проверка страницы изменения пароля для гостей'
        response = self.guest_client.get('/auth/password_change/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND,
                         'ОШИБКА: страница изменения работает \
                              у не авторизированных!')

    def test_password_change_autorization(self):
        'Проверка страницы изменения пароля авторизированных'
        response = self.authorized_client.get('/auth/password_change/')
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'ОШИБКА: страница изменения пароля не работает!')

    def test_password_change_autorization_done(self):
        'Проверка страницы успешного изменения пароля для авторизированных'
        response = self.authorized_client.get('/auth/password_change/done/')
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'ОШИБКА: Страница успешного изменения пароля \
    работает для неавторизированных!')

    def test_password_reset_gost(self):
        'Проверка страницы восстановления пароля для гостей'
        response = self.guest_client.get('/auth/password_reset/')
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'ОШИБКА: Страница восстановления \
    не работает для гостей!')

    def test_password_reset_autorization(self):
        'Проверка страницы восстановления пароля для авторизированных'
        response = self.authorized_client.get('/auth/password_reset/')
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'ОШИБКА: Страница восстановления \
    не работает!')

    def test_password_reset_gost_done(self):
        'Проверка страницы подтверждения восстановления пароля для гостей'
        response = self.guest_client.get('/auth/password_reset/done/')
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'ОШИБКА: Страница подтверждения \
    восстановления пароля работает для гостей!')

    def test_password_reset_autirization_done(self):
        'Проверка страницы подтверждения восстановления пароля'
        response = self.authorized_client.get('/auth/password_reset/done/')
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'ОШИБКА: Страница подтверждения \
    восстановления пароля не работает!')

    def test_urls_uses_correct_template(self):
        'URL-адрес использует соответствующий шаблон для авторизированных'
        # Шаблоны по адресам
        templates_url_names = {
            '/auth/signup/': 'users/signup.html',
            '/auth/logout/': 'users/logged_out.html',
            '/auth/login/': 'users/login.html',
            '/auth/password_reset/': 'users/password_reset_form.html',
            '/auth/password_reset/done/': 'users/password_reset_done.html',
            '/auth/password_change/': 'users/password_change_form.html',
            '/auth/password_change/done/': 'users/password_change_done.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
