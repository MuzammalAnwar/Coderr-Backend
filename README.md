# Coderr – Backend (Django + DRF)

This repository contains the backend implementation of the project **Coderr**, built with **Django** and **Django REST Framework (DRF)**.

---

## 🛠️ Tech Stack
- **Python 3.12**
- **Django 5.x**
- **Django REST Framework (DRF)**
- **DRF Token Authentication**
- **SQLite** (default local database)

---

## Getting Started

Follow these steps to set up and run the backend locally.

### 1. Clone the repository
```bash
git clone https://github.com/MuzammalAnwar/Coderr-Backend.git
```
```bash
cd Coderr-Backend
```
### 2. Create and activate a virtual environment
### Windows (PowerShell)
```bash
python -m venv env
```
```bash
"env\Scripts\activate"
```
### Linux / macOS
```bash
python3 -m venv env
```
```bash
source env/bin/activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Apply database migrations
```bash
python manage.py migrate
python manage.py createsuperuser  # optional
```
### 5. Run the development server
```bash
python manage.py runserver
#http://127.0.0.1:8000/
```
