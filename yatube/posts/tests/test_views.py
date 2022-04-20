import shutil
import tempfile
from django.conf import settings
from django.test import TestCase, Client, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import forms
from xmlrpc.client import Boolean
from ..models import Post
from ..models import Group
from ..models import Follow

User = get_user_model()

# Создаем временную папку для медиа-файлов;
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД:
        # Пользователь
        cls.user = User.objects.create_user(username='TestName')
        cls.user2 = User.objects.create_user(username='TestNames')
        # Группа
        cls.group = Group.objects.create(
            title='Группа',
            slug='t_slug',
        )
        # Картинка
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        # Пост от пользователя TestName
        cls.post = Post.objects.create(
            text='Пост1',
            author=User.objects.get(username='TestName'),
            group=cls.group,
            image=cls.uploaded
        )
        cls.follow = Follow.objects.create(
            user=cls.user2,
            author=cls.user)

        cls.urls = {
            'index': reverse('posts:index'),
            'group_list': reverse(
                'posts:group_list',
                kwargs={'slug': cls.group.slug}
            ),
            'profile': reverse(
                'posts:profile',
                kwargs={'username': cls.user.username}
            ),
            'post_detail': reverse(
                'posts:post_detail',
                kwargs={'post_id': cls.post.id}
            ),
            'post_create': reverse('posts:post_create'),
            'post_edit': reverse(
                'posts:post_edit',
                kwargs={'post_id': cls.post.id}
            ),
        }
        cls.form_data = {
            'user': cls.user2.username,
            'author': cls.post.author
        }

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Модуль shutil - библиотека Python с удобными инструментами
        # для управления файлами и директориями:
        # создание, удаление, копирование, перемещение  папок и файлов
        # Метод shutil.rmtree удаляет директорию и всё её содержимое
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        # Создаем авторизованные клиенты
        self.authorized_client = Client()
        self.authorized_client2 = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client2.force_login(self.user2)

    def test__template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            self.urls['index']: 'posts/index.html',
            self.urls['group_list']: 'posts/group_list.html',
            self.urls['profile']: 'posts/profile.html',
            self.urls['post_detail']: 'posts/post_detail.html',
            self.urls['post_create']: 'posts/post_create.html',
            self.urls['post_edit']: 'posts/post_create.html',
        }
        # Проверяем, что при обращении к name вызывается
        # соответствующий HTML-шаблон
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_group_list_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:group_list',
                                              kwargs={'slug': self.group.slug})
                                              )
        # Взяли первый элемент из списка и проверили, что его содержание
        # совпадает с ожидаемым
        first_object = response.context['page_obj'][0]
        index_text = first_object.text
        index_author = first_object.author.username
        test_image = first_object.image
        index_group = first_object.group.slug
        self.assertEqual(index_text, self.post.text, 'Ошибка: Text поста')
        self.assertEqual(index_author, self.post.author.username,
                         'Ошибка: Username')
        self.assertEqual(index_group, self.post.group.slug, 'Ошибка: Slug')
        self.assertEqual(test_image, self.post.image,
                         'ОШИБКА: Картинки нет')

    def test_index_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.urls['index'])
        # Взяли первый элемент из списка и проверили, что его содержание
        # совпадает с ожидаемым
        first_object = response.context['page_obj'][0]
        index_text = first_object.text
        index_author = first_object.author.username
        test_image = first_object.image
        index_group = first_object.group.slug
        self.assertEqual(index_text, self.post.text, 'Ошибка: Text поста')
        self.assertEqual(index_author, self.post.author.username,
                         'Ошибка: Username')
        self.assertEqual(index_group, self.post.group.slug, 'Ошибка: Slug')
        self.assertEqual(test_image, self.post.image,
                         'ОШИБКА: Картинки нет')

    def test_profile_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:profile',
                                              kwargs={
                                                  'username': self.post.
                                                  author.username})
                                              )
        first_object = response.context['page_obj'][0]
        # Теперь проверяем, что что содержимое постов на странице
        test_text_0 = first_object.text
        test_author_0 = first_object.author
        test_image_0 = first_object.image
        test_title_0 = first_object.group.title
        test_group_slug_0 = first_object.group.slug
        self.assertEqual(test_text_0, self.post.text,
                         'ОШИБКА: Текст не совпадает!')
        self.assertEqual(test_author_0, self.post.author,
                         'ОШИБКА: Автор не совпадает!')
        self.assertEqual(test_title_0, self.group.title,
                         'ОШИБКА: Title не совпадают!')
        self.assertEqual(test_group_slug_0, self.group.slug,
                         'ОШИБКА: Слаг не совпадает!')
        self.assertEqual(test_image_0, self.post.image,
                         'ОШИБКА: Картинки нет')

    def test_post_detail_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = (self.authorized_client.get(self.urls['post_detail']))
        context = response.context.get('post')
        self.assertEqual(context.text, self.post.text)
        self.assertEqual(context.id, self.post.id)
        self.assertEqual(context.image, self.post.image)
        self.assertEqual(context.author.username,
                         self.post.author.username)
        self.assertEqual(context.group,
                         self.post.group)

    def test_post_create_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.urls['post_create'])
        # Словарь ожидаемых типов полей формы:
        # указываем, объектами какого класса должны быть поля формы
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        # Проверяем, что типы полей формы в словаре context
        # соответствуют ожиданиям
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)

    def test_post_edit_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.urls['post_edit'])
        context = response.context.get('post')
        self.assertEqual(context.text, self.post.text)
        self.assertEqual(context.id, self.post.id)
        self.assertEqual(context.author.username,
                         self.post.author.username)
        # Словарь ожидаемых типов полей формы:
        # указываем, объектами какого класса должны быть поля формы
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        # Проверяем, что типы полей формы в словаре
        # context соответствуют ожиданиям
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)
                is_edit = response.context['is_edit']
                self.assertIsInstance(is_edit, Boolean)
                self.assertAlmostEqual(is_edit, True)

    def test_index_cach(self):
        """Проверяем сохраняются ли посты в кэш на главной странице"""
        response = self.authorized_client.get(self.urls['index']).content
        Post.objects.all().delete()
        self.assertEqual(len(Post.objects.all()), 0)
        new_content = response
        self.assertEquals(response, new_content)

    def test_following_1(self):
        """Подписка на авторов работает"""
        follow_count = Follow.objects.count()

        # Подписываемся
        response = self.authorized_client.post(reverse('posts:profile_follow',
                                               kwargs={
                                                   'username':
                                                   self.user2.username}),
                                               data=self.form_data,
                                               follow=True)
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('posts:profile',
                                               kwargs={
                                                   'username':
                                                   f'{self.user2.username}'}))
        # Проверяем, сработала ли подписка
        self.assertEqual(Follow.objects.count(), follow_count + 1,
                         'Ошибка:Число подписчиков не увеличелось..')

        # Проверяем что подписки появляются у подписавшегося.
        follower = Post.objects.filter(author__following__user=self.user2
                                       ).exists()
        self.assertTrue(follower)

    def test_following_2(self):
        """Отписка от автора работает"""
        follow_count = Follow.objects.count()
        response = self.authorized_client2.post(reverse(
                                                'posts:profile_unfollow',
                                                kwargs={
                                                    'username':
                                                    self.post.author.username}
                                                ))
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('posts:profile',
                             kwargs={
                                 'username':
                                 f'{self.post.author.username}'}))
        self.assertEqual(Follow.objects.count(), follow_count - 1,
                         'Ошибка:Число подписчиков не уменьшелось..')

    def test_following_3(self):
        """Проверяем что посты автора не появляются у не подписанного
         пользователя."""

        ne_follower = Post.objects.filter(author__following__user=self.user
                                          ).exists()
        self.assertFalse(ne_follower)

    def test_following_4(self):
        """Проверяем что посты автора появляются у подписанного."""
        follower = Post.objects.filter(author__following__user=self.user2
                                       ).exists()
        self.assertTrue(follower)


class ContextPostViewsTest(TestCase):
    """Класс для проверки Paginator приложения posts."""
    all_post_count = 12
    post_one = 1
    Paginator = 10
    SUM_OF_POSTS = all_post_count - Paginator

    @classmethod
    def setUpClass(cls):
        """Добавляем во временную базу данных обыекты:
        2 пользователя, 2 группы и 12 постов."""
        super().setUpClass()
        cls.user = User.objects.create_user(username='author')
        cls.user_2 = User.objects.create_user(username='author_2')
        cls.group_1 = Group.objects.create(
            title='Тестовая группа 1',
            slug='test_slug_1',
            description='Тестовое описание',
        )
        cls.group_2 = Group.objects.create(
            title='Тестовая группа 2',
            slug='test_slug_2',
            description='Тестовое описание',
        )
        Post.objects.create(
            author=cls.user,
            text='Тестовый пост №1',
            group=cls.group_1
        )
        number_of_posts = cls.all_post_count
        Post.objects.bulk_create(
            Post(
                author=cls.user_2,
                text=f'Тестовый пост №2_{i + 1}',
                group=cls.group_2
            ) for i in range(number_of_posts)
        )

    def setUp(self):
        """Авторизуем автора поста."""
        self.authorized_author = Client()
        self.authorized_author.force_login(self.user)

    def test_index_page_1(self):
        """В Шаблоне index стра.1 пагинатор работает верно."""
        response = self.client.get(reverse('posts:index'))
        context = response.context['page_obj']
        # Проверка: количество постов на первой странице равно 10.
        self.assertEqual(len(context), self.Paginator)

    def test_index_page_2(self):
        """В Шаблоне index стра.2 пагинатор работает верно."""
        # Проверка: на второй странице должно быть три поста.
        response = self.client.get(reverse('posts:index') + '?page=2')
        context = response.context['page_obj']
        self.assertEqual(len(context),
                         (self.SUM_OF_POSTS + self.post_one))

    def test_group_list_page_1(self):
        """В Шаблоне group_list стра.1 пагинатор работает верно."""
        response = self.client.get(reverse('posts:group_list',
                                           kwargs={'slug': self.group_2.slug}))
        context = response.context['page_obj']
        # Проверка: количество постов на первой странице равно 10.
        self.assertEqual(len(context), self.Paginator)

    def test_group_list_page_2(self):
        """В Шаблоне group_list стра.2 пагинатор работает верно."""
        response = self.client.get(reverse('posts:group_list',
                                           kwargs={'slug': self.group_2.slug}
                                           ) + '?page=2')
        context = response.context['page_obj']
        self.assertEqual(len(context), self.SUM_OF_POSTS)

    def test_profile(self):
        """Проверяем количество постов на первой странице profile
        и принадлежность всех постов одному автору"""
        number_of_posts_per_page = (
            self.Paginator,
            self.all_post_count - self.Paginator,
        )
        for page_number in range(len(number_of_posts_per_page)):
            with self.subTest(page_number=page_number):
                page_url = reverse(
                    'posts:profile', kwargs={
                        'username': f'{self.user_2.username}'
                    }
                ) + f'?page={page_number + 1}'
                response = self.authorized_author.get(page_url)
                context = response.context['page_obj']
                self.assertEqual(
                    len(context),
                    number_of_posts_per_page[page_number],
                )
                for post in context:
                    self.assertEqual(
                        post.author.username,
                        self.user_2.username,
                    )
