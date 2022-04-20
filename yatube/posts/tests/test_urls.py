from ..models import Group, Post
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from http import HTTPStatus
from django.urls import reverse


User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД для проверки доступности адреса Group/test-slug/
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='t_slag',
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя 1
        self.user = User.objects.create_user(username='TestName')
        # Создаем пользователя 2
        self.user2 = User.objects.create_user(username='TestNames')
        # Создаем два клиент
        self.authorized_client = Client()
        self.authorized_client2 = Client()
        # Авторизуем пользователей,
        # для проверки редактирования постов не создателем
        self.authorized_client.force_login(self.user)
        self.authorized_client2.force_login(self.user2)
        # Создаем пост  для пользовател TestName
        self.post = Post.objects.create(
            text='Тестовый пост',
            author=User.objects.get(username='TestName'),
        )

    def test_homepage(self):
        'Проверка домашней страницы для не авторизированных'
        response = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'ОШИБКА: Домашняя страница работает не верно!')

    def test_grouppage(self):
        'Проверка страниц групп для не авторизированных'
        response = self.guest_client.get(reverse('posts:group_list',
                                         kwargs={'slug': f'{self.group.slug}'})
                                         )
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'ОШИБКА: страница /group/<slug> работает не верно!')

    def test_profileppage(self):
        'Проверка страницы профиля для не авторизированных'
        response = self.guest_client.get(reverse('posts:profile',
                                         kwargs={'username':
                                                 f'{self.user.username}'})
                                         )
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'ОШИБКА: страница профилей не работает!')

    def test_post_page(self):
        'Проверка страницы просмотра постов для не авторизированных'
        response = self.guest_client.get(reverse('posts:post_detail',
                                         kwargs={'post_id': f'{self.post.id}'})
                                         )
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'ОШИБКА: Страница просмотра постов не работает!')

    def test_post_no_edit_page(self):
        'Проверка страницы редактирования постов для не авторизированных'
        response = self.guest_client.get(reverse('posts:post_edit',
                                         kwargs={'post_id': f'{self.post.id}'})
                                         )
        self.assertEqual(response.status_code, HTTPStatus.FOUND,
                         'ОШИБКА: Редактирует не авторизированный!')

    def test_post_edit_page(self):
        'Проверка страницы редактирования постов для автора'
        response = self.authorized_client.get(reverse('posts:post_edit',
                                              kwargs={'post_id':
                                                      f'{self.post.id}'})
                                              )
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'ОШИБКА: Редактирует не автор!')

    def test_post_edit_neauthor_page(self):
        'Проверка страницы редактирования постов для автора'
        response = self.authorized_client2.get(reverse('posts:post_edit',
                                               kwargs={'post_id':
                                                       f'{self.post.id}'})
                                               )
        self.assertEqual(response.status_code, HTTPStatus.FOUND,
                         'ОШИБКА: Редактирует не создатель!')

    def test_create_post_noautorization(self):
        'Проверка страницы добавления постов для не авторизированных'
        response = self.guest_client.get(reverse('posts:post_create'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND,
                         'ОШИБКА: Добавляет не авторизированный!')

    def test_create_post(self):
        'Проверка страницы добавления постов для авторизированных'
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK,
                         'ОШИБКА: Добавление постов не работает!')

    def test_404(self):
        'Проверка страницы добавления постов для авторизированных'
        erroes = ('/unexisting_page/')
        response = self.authorized_client.get(erroes)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND,
                         'ОШИБКА: Добавление постов не работает!')

    def test_urls_uses_correct_template(self):
        'URL-адрес использует соответствующий шаблон для авторизированных'
        # Шаблоны по адресам
        urls = {
            'index': reverse('posts:index'),
            'group_list': reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}
            ),
            'profile': reverse(
                'posts:profile',
                kwargs={'username': self.user.username}
            ),
            'post_detail': reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}
            ),
            'post_create': reverse('posts:post_create'),
            'post_edit': reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}
            ),
        }
        templates_url_names = {
            urls['index']: 'posts/index.html',
            urls['group_list']: 'posts/group_list.html',
            urls['profile']: 'posts/profile.html',
            urls['post_detail']: 'posts/post_detail.html',
            urls['post_edit']: 'posts/post_create.html',
            urls['post_create']: 'posts/post_create.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
