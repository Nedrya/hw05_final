import shutil
import tempfile
from django.conf import settings
from django.test import TestCase, Client, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Post, Comment
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

# Создаем временную папку для медиа-файлов;
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class FormTest(TestCase):
    '''Формы работают верно!'''

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создали пользователя
        cls.user = User.objects.create_user(username='TestName')
        # Создаем запись в базе данных с постом
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
        cls.post = Post.objects.create(
            text='Пост1',
            author=User.objects.get(username='TestName'),
            group=None,
            image=cls.uploaded
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Модуль shutil - библиотека Python с удобными инструментами
        # для управления файлами и директориями:
        # создание, удаление, копирование, перемещение  папок и файлов
        # Метод shutil.rmtree удаляет директорию и всё её содержимое
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        # Залогинили пользователя TestName
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.guest_client = Client()

    def test_creating_records(self):
        'Проверка создания записей с картинкой'
        post_count = Post.objects.count()
        form_data = {
            'text': 'Пост2',
            'author': 'TestName',
            'images': self.uploaded
        }
        response = self.authorized_client.post(reverse('posts:post_create'),
                                               data=form_data,
                                               follow=True)
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('posts:profile',
                                               kwargs={
                                                   'username':
                                                   f'{self.user.username}'}))
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), post_count + 1,
                         'Ошибка:Число постов не увеличелось..')

        # Проверяем есть ли в посте картинка
        self.assertIsNotNone(Post.objects.get(id=2).image,
                             'Ошибка: картинка отсутствует..')

    def test_edit_records(self):
        'Проверка редактирования записей'
        form_data = {
            'text': 'Отредактировано',
            'author': 'TestName',
        }
        response = self.authorized_client.post(reverse('posts:post_edit',
                                               kwargs={
                                                   'post_id': self.post.id}),
                                               data=form_data,
                                               follow=True)
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('posts:post_detail',
                                               kwargs={
                                                   'post_id':
                                                   f'{self.post.id}'}))
        # Проверяем изменилась ли запись в БЛ
        self.assertEqual(Post.objects.all()[0].text, form_data['text'],
                         'Ошибка: БД не изменилось!')

    def test_comment_posts(self):
        'Проверка создания комментария'
        comment_count = Comment.objects.count()
        form_data = {
            'text': 'Коммент',
            'author_id': self.user.id,
            'post_id': self.post.id
        }
        response = self.authorized_client.post(reverse('posts:add_comment',
                                               kwargs={
                                                   'post_id': self.post.id}),
                                               data=form_data,
                                               follow=True)
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('posts:post_detail',
                                               kwargs={
                                                   'post_id':
                                                   f'{self.post.id}'}))
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Comment.objects.count(), comment_count + 1,
                         'Ошибка:Число постов не увеличелось..')

    def test_comment_posts_guost(self):
        'Проверка создания комментария не авторизированного'
        author = self.user.id
        post = self.post.id
        comment_count = Comment.objects.count()
        form_data = {
            'text': 'Коммент',
            'author_id': author,
            'post_id': post
        }
        response = self.guest_client.post(reverse('posts:add_comment',
                                          kwargs={
                                                  'post_id': self.post.id}),
                                          data=form_data,
                                          follow=True)
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('users:login')
                             + f'?next=/posts/{self.post.id}/comment/')
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Comment.objects.count(), comment_count,
                         'Ошибка:Число постов увеличелось..')
