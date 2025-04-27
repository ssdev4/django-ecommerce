# 🛒 Django eCommerce Project

A full-featured eCommerce web application built with Django. This project is designed for scalability, clean architecture, and includes features like item listing, shopping cart, checkout, inventory management, custom dashboard, and live chat.

---

## ✅ Current Phase: Initial Setup

### 🔧 Tech Stack
- **Backend**: Django 4.2.20, daphne, channels, Redis, Docker
- **Database**: SQLite (for development)
- **Frontend**: Bootstrap 5 (via CDN)
- **Language**: Python 3.9.6
- **OS**: macOS

---

## 📁 Project Setup
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## 📁 Run Project (Development)

```
python manage.py makemigrations
python manage.py migrate
python manage.py migrate django_celery_beat
python manage.py runserver
```

## Email Testing (Development)
```
docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog
```

## Run Celery
```
celery -A ecommerce_project worker --loglevel=info
```
## Run Celery Beat
```
celery -A ecommerce_project beat --loglevel=info
```
## Run Flower
```
celery -A ecommerce_project flower
```

## Or run both via bash script
```
./start-celery.sh
```

## Prod Deploy

For production, typically run Daphne explicitly
`daphne -b 0.0.0.0 -p 8000 ecommerce_project.asgi:application`
behind a reverse proxy (Nginx, etc.).

For more detail
https://docs.djangoproject.com/en/5.2/howto/deployment/

