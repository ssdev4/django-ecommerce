# 🛒 Django eCommerce Project

A full-featured eCommerce web application built with Django. This project is designed for scalability, clean architecture, and includes features like item listing, shopping cart, checkout, inventory management, custom dashboard, and live chat.

---

## ✅ Current Phase: Initial Setup

### 🔧 Tech Stack
- **Backend**: Django 4.2.20
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
## 📁 This is using dphane to support websocket
to run project
```
DJANGO_SETTINGS_MODULE=ecommerce_project.settings daphne -p 8000 ecommerce_project.asgi:application
```
