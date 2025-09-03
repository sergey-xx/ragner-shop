# pubg_bot

PUBG_SHOP на Django и aiogram


Для запуска требуется установка docker и docker compose.

1. Скопировать проект на сервер
2. переименовать файл .env.example в .env и заполнить переменные
3. в папке с проектом выполнить команду
```
sudo docker compose up -d
```
4. Cоздать пользователя для входа в админ-панель
```
 sudo docker compose exec admin_panel python manage.py createsuperuser
```
После чего ввести имя, почту (можно выдуманную, но валидную) и пароль для админки

Загрузить базовые конфигурации
```
sudo docker compose exec admin_panel python manage.py load_config
```

## Пересборка контейнера
```
sudo docker compose down
sudo docker compose up -d --build
```

## Локальный запуск Celery на Windows

```
celery -A backend worker --loglevel info --pool=solo
```


Создать моковые данные:

```
python manage.py mockchats
python manage.py mockitems

```