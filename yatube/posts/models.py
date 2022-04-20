from django.db import models
# Из модуля auth импортируем функцию get_user_model
from django.contrib.auth import get_user_model

User = get_user_model()


class Group (models.Model):
    '''Модель создания группы'''
    title = models.CharField(max_length=200, verbose_name='Название группы')
    slug = models.SlugField(max_length=255,
                            unique=True,
                            db_index=True,
                            verbose_name='URL',
                            )
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    '''Модель создания поста'''
    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
        db_index=True
    )
    сomment = models.ForeignKey(
        'Comment',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='comment',
        verbose_name='Коментарии',
        help_text='Коментарии к  посту',
    )

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст коментария',
        help_text='Напишите текст коментария'
    )
    created = models.DateTimeField(
        'date_created',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower')
    author = models.ForeignKey(User,
                               related_name='following',
                               on_delete=models.CASCADE,
                               )
