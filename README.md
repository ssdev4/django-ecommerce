# 🛒 Django eCommerce Project

A full-featured eCommerce web application built with Django. This project is designed for scalability, clean architecture, and includes features like item listing, shopping cart, checkout, inventory management, custom dashboard, and live chat.

---

## ✅ Current Phase: Initial Setup

### 🔧 Tech Stack
- **Backend**: Django 4.2.20, daphne, channels, Redis
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
python manage.py runserver
```

## Prod Deploy

For production, typically run Daphne explicitly 
`daphne -b 0.0.0.0 -p 8000 ecommerce_project.asgi:application`
behind a reverse proxy (Nginx, etc.).

For more detail
https://docs.djangoproject.com/en/5.2/howto/deployment/

