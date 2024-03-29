### О проекте:

Проект «Yatube» с авторизацией на Django, чтением из БД и записью в неё, генерацией индивидуальных страниц пользователей.
В качестве фреймворка использовался Django 2.2.16.
Дополнительно использовались следующие пакеты: Faker 12.0.1, Mixer 7.1.2, Pillow 8.3.1, Sorl-thumbnail 12.7.0.


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Nedrya/hw05_final
```

```
cd hw05_final
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py makemigrations
```
```
python3 manage.py migrate
```

Заполнить базу данных тестовыми данными:

```
python3 manage.py install_bd
```


Запустить проект:

```
python3 manage.py runserver
```


### Информация:

1) С помощью sorl-thumbnail выведены иллюстрации к постам:

• в шаблон главной страницы
• в шаблон профайла автора
• в шаблон страницы группы
• на отдельную страницу поста


Написаны тесты, которые проверяют:

• при выводе поста с картинкой изображение передаётся в словаре context:
    1- на главную страницу,
    2- на страницу профайла,
    3- на страницу группы,
    4- на отдельную страницу поста;
• при отправке поста с картинкой через форму PostForm создаётся запись в базе данных;


2) Реализована система комментариев.


Написана система комментирования записей. На странице поста под текстом записи выводится форма для отправки комментария, а ниже — список комментариев. Комментировать могут только авторизованные пользователи. Работоспособность модуля протестирована.

3) Кеширование главной страницы.

Список постов на главной странице сайта хранится в кэше и обновляется раз в 20 секунд.

4) Тест проверки кеширования.

Написан тест для проверки кеширования главной страницы. Логика теста: при удалении записи из базы, она остаётся в response.content главной страницы до тех пор, пока кэш не будет очищен принудительно.

5) Система подписки.

Добавлена система подписки на авторов и создана лента их постов.

6) Тесты подписки.

Написаны тесты, проверяющие работу сервиса:

• Авторизованный пользователь может подписываться на других пользователей и удалять их из подписок.
• Новая запись пользователя появляется в ленте тех, кто на него подписан и не появляется в ленте тех, кто не подписан.

Автор проекта: Недря Сергей.




