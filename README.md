# Тестовое задание
## Эхо Павел Дмитриевич 

1. Разверните виртуальное окружение и создайте проект с названием ```tp_znakomstva```
2. Скачайте архив и распакуйте его в созданную директорию (можете сделать конечно командами git)
3. Установите зависимости ```pip install -r requirements.txt```
4. Так как я решил использовать библиотеку по водяным знакам, то установил зависимость ```django-watermark==0.1.8```. Если Вы используете свежие версии Django, то измените импорты в модели, которая расположена по пути ```tp_znakomstva\venv\Lib\site-packages\watermarker\models.py```:

``` # from django.utils.translation import ugettext_lazy as _```

``` # from django.utils.encoding import python_2_unicode_compatible```

```from django.utils.translation import gettext_lazy as _```

```from six import python_2_unicode_compatible```

4. Создайте миграции ```python manage.py makemigrations```, а затем ```python manage.py makemigrations members```
5. Проведите миграции ```python manage.py migrate```
6. Соберите все статик файлы в проекте ```python manage.py collectstatic```
7. Если захотите загрузить в БД тестовые данные, то ```python manage.py loaddata exclude_db.json```
8. Запустите локальный сервер ```python manage.py runserver```
9. Добавил реализацию РЕСТ
10. Добавил тестирование по РЕСТ с помощью Swagger
11. Проверяйте реализацию тестового задания.
