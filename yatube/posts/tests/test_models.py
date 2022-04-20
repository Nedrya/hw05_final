from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
        )

    def test_models_have_correct_object_group(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        group = self.group  # Обратите внимание на синтаксис
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group),
                         'ОШИБКА:__Str__ в Group ')

    def test_models_have_correct_object_post(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        group = self.post  # Обратите внимание на синтаксис
        expected_object_name = group.text[:15]
        self.assertEqual(expected_object_name, str(group),
                         'ОШИБКА:__Str__ в Post ')

    def test_models_text_post(self):
        """в моделе Post - verbose_name поля title совпадает с ожидаемым."""
        group = self.post
        # Получаем из свойста класса Post значение help_text для text
        verbose = group._meta.get_field('text').help_text
        self.assertEqual(verbose, 'Введите текст поста',
                         'ОШИБКА: help_text в post.text ')

    def test_models_text_post(self):
        """в моделе Post - verbose_name поля title совпадает с ожидаемым."""
        group = self.post
        # Получаем из свойста класса Post значение verbose_name для text
        verbose = group._meta.get_field('text').verbose_name
        self.assertEqual(verbose, 'Текст поста',
                         'ОШИБКА: verbose_name в post.text ')

    def test_models_text_post(self):
        """в моделе Post - verbose_name поля title совпадает с ожидаемым."""
        group = self.post
        # Получаем из свойста класса Post значение verbose_name для text
        verbose = group._meta.get_field('text').verbose_name
        self.assertEqual(verbose, 'Текст поста',
                         'ОШИБКА: verbose_name в post.text ')

    def test_models_pub_date_post(self):
        """в моделе Post - verbose_name поля pub_date совпадает с ожидаемым."""
        group = self.post
        # Получаем из свойста класса Post значение verbose_name для text
        verbose = group._meta.get_field('pub_date').verbose_name
        self.assertEqual(verbose, 'Дата публикации',
                         'ОШИБКА: verbose_name в post.pub_date ')

    def test_models_author_post(self):
        """в моделе Post - verbose_name поля Author совпадает с ожидаемым."""
        group = self.post
        # Получаем из свойста класса Post значение verbose_name для text
        verbose = group._meta.get_field('author').verbose_name
        self.assertEqual(verbose, 'Автор',
                         'ОШИБКА: verbose_name в post.Author ')

    def test_models_group_post_verbose_name(self):
        """в моделе Post - verbose_name поля group совпадает с ожидаемым."""
        group = self.post
        # Получаем из свойста класса Post значение verbose_name для text
        verbose = group._meta.get_field('group').verbose_name
        self.assertEqual(verbose, 'Группа',
                         'ОШИБКА: verbose_name в post.group ')

    def test_models_group_post_help_text(self):
        """в моделе Post - help_text поля group совпадает с ожидаемым."""
        group = self.post
        # Получаем из свойста класса Post значение verbose_name для text
        verbose = group._meta.get_field('group').help_text
        self.assertEqual(verbose, 'Группа, к которой будет относиться пост',
                         'ОШИБКА: help_text в post.group ')
