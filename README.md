# MailCampaign

MailCampaign — это веб-приложение для массовой рассылки почтовых сообщений.

## Используемые технологии

### Backend:
- Python 2.7
- Django 1.9.9

### Frontend:
- jQuery
- Bootstrap

## Рабочие URL

- `/mailings/` — список рассылок
- `/subscribers/` — список подписчиков
- `/messages/` — список сообщений
- `/admin/` — админ-панель

## Возможные улучшения

Можно запустить проект через Docker Compose, но изначально он разрабатывался без Docker, поэтому переделывать было лень.

## Быстрый старт

### 1. Клонирование репозитория
```sh
git clone https://github.com/EshKG/mailcampaign.git
cd mailcampaign
```

### 2. Активация виртуального окружения
```sh
source venv/bin/activate
```

### 3. Установка зависимостей и миграции
```sh
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

### 4. Настройка переменных среды

Перед запуском сервера, измените переменные в `mailcampaign/settings.py`:

```python
SITE_URL = "ваш урл"

# SMTP настройки
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465  # 587 для TLS, 465 для SSL
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'abdullaev@test.ru'
EMAIL_HOST_PASSWORD = 'yourpass'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Настройки Celery
BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_TIMEZONE = 'Europe/Moscow'
```

## Запуск сервиса

### 1. Запуск Redis (используется Docker)
```sh
docker run -d --name redis -p 6379:6379 --network host redis
```

### 2. Запуск Django сервера
```sh
python manage.py runserver 0.0.0.0:8000
```

### 3. Запуск Celery
```sh
celery -A mailcampaign worker --loglevel=info
```

📌 Django и Celery рекомендуется запускать в отдельных терминалах (например, в WSL).

## Интерфейс приложения

### 📩 Страница "Список рассылок" (`/mailings/`)
Выводит список всех рассылок и кнопку для создания новой рассылки.

### 📌 Модальное окно создания рассылки
Появляется при нажатии кнопки "Создать рассылку".

### 👥 Страница "Список подписчиков" (`/subscribers/`)
Выводит список подписчиков и кнопку для их добавления.

### ➕ Модальное окно добавления подписчиков
Позволяет добавить подписчика. В случае ошибки отображает alert.

## ❗ Замечания

- Используется **Python 2.7** и **Django 1.9.9** (устаревшие версии).
- Запуск в **Docker Compose** значительно упростил бы настройку проекта.
- В коде возможны потенциальные уязвимости из-за устаревших зависимостей.

📌 **Рекомендация**: Обновить стек технологий до **Python 3** и **Django 4+**.
Все создано мной с использованием моего опыта, онлайн документации и ChatGPT 
