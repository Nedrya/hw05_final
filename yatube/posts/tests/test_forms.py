from django.test import TestCase, Client
from ..models import Post, Comment
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class FormTest(TestCase):
    '''Формы работают верно!'''

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создали пользователя
        cls.user = User.objects.create_user(username='TestName')
        # Создаем запись в базе данных с постом
        cls.post = Post.objects.create(
            text='Пост1',
            author=User.objects.get(username='TestName'),
            group=None
        )

    def setUp(self):
        # Залогинили пользователя TestName
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.guest_client = Client()

    def test_creating_records(self):
        'Проверка создания записей'
        post_count = Post.objects.count()
        form_data = {
            'text': 'Пост2',
            'author': 'TestName',
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
