# Coderr – Backend (Django + DRF)

This repository contains the backend implementation of the project **Coderr**, built with **Django** and **Django REST Framework (DRF)**.

## Features

- **User Roles**
  - **Customer Users** – can browse offers, place orders, and manage their own requests  
  - **Business Users** – can create and publish offers, update availability, and manage incoming customer orders  

- **Marketplace**
  - Publicly accessible list of offers visible to all visitors  
  - Filterable and browsable interface for quick discovery of software services  

- **Authentication & Permissions**
  - Secure user registration & login system  
  - Role-based access: only business users can create offers, only customers can place orders  
  - Django Admin panel for superusers to oversee and manage all users and offers  

- **Offer Management (Business Users)**
  - Create, edit, and delete software-related offers  
  - Define price, description, and delivery time for each offer  
  - View and manage customer orders related to their offers  

- **Order Management (Customer Users)**
  - Place orders directly on published offers  
  - Track order status and progress  
  - Manage their own order history

## Deployment

- The backend is deployed on a Google Cloud VM using the following stack:

- Gunicorn – WSGI server for running Django

- Nginx – reverse proxy handling client requests and SSL termination

- Supervisor – process manager to keep Gunicorn running

- Certbot (Let’s Encrypt) – automatic HTTPS certificates

The API documentation is accessible
👉 [here](https://coderr-api.muzammal-anwar.at/api/docs/)

The API schema can be downloaded
👉 [here](https://coderr-api.muzammal-anwar.at/api/schema/)

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
