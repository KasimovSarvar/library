# Library Management System 📚

This is a Django-based project for managing books, users, and borrowing logic.

## Features

- User authentication
- Book CRUD
- Search and filtering
- API documentation (Swagger with drf-yasg)

## Tech Stack

- Django
- Django REST Framework
- drf-yasg (Swagger API)
- SimpleJWT for authentication

## How to Run

```bash
git clone https://github.com/KasimovSarvar/library.git
cd library
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
