# 🔗 URL Shortener API

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15-red.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-✓-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-quality URL Shortener API built with **Django 5**, **Django REST Framework**, **PostgreSQL**, **JWT Authentication**, and **Docker**. Designed with clean architecture, security best practices, and scalability in mind.

---

## ✨ Features

- **User Authentication** — Registration and login with JWT (JSON Web Tokens)
- **URL Shortening** — Generate secure, random short codes using cryptographic randomness (`secrets` module)
- **Click Analytics** — Atomic click counting with race-condition protection via Django `F()` expressions
- **URL Management** — List and delete your shortened URLs with strict ownership enforcement
- **Auto Documentation** — Interactive Swagger UI generated automatically from DRF views
- **Docker Support** — One-command setup with Docker Compose
- **Clean Architecture** — Modular Django apps: `accounts/` and `urls/`

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Framework | Django 5.0 + Django REST Framework 3.15 |
| Database | PostgreSQL 16 |
| Authentication | JWT (djangorestframework-simplejwt) |
| API Docs | drf-spectacular (OpenAPI 3.0 / Swagger) |
| Containerization | Docker + Docker Compose |
| WSGI Server | Gunicorn |

---

## 🏗 Architecture
┌─────────────┐      ┌─────────────┐      ┌─────────────────────────────┐
│   Client    │──────▶   Nginx     │──────▶  Gunicorn (WSGI)            │
│  / curl     │      │  (reverse   │      │  └── Django 5               │
└─────────────┘      │   proxy)    │      │       ├── DRF (Serializers) │
└─────────────┘      │       ├── JWT Middleware      │
│       ├── Views (Business)  │
│       └── Models (ORM)      │
│              │              │
└──────────────┼──────────────┘
│
┌──────▼──────┐
│  PostgreSQL │
│    (RDS)    │
└─────────────┘


The project follows **Django's app-based modular architecture**:

- **`config/`** — Project settings, WSGI entry point, root URL routing
- **`accounts/`** — User registration and JWT token management
- **`urls/`** — Core domain: URL shortening, redirect logic, click analytics

---

## 🗄 Database Schema

### `auth_user` (Django built-in)

| Field | Type | Notes |
|-------|------|-------|
| `id` | PK | Auto-increment |
| `username` | `VARCHAR(150)` | Unique, required |
| `email` | `VARCHAR(254)` | Validated for uniqueness |
| `password` | `VARCHAR(128)` | Hashed with PBKDF2 |

### `urls_shorturl`

| Field | Type | Constraints |
|-------|------|-------------|
| `id` | PK | BigAutoField |
| `user_id` | FK → `auth_user` | `ON DELETE CASCADE`, indexed |
| `original_url` | `VARCHAR(2048)` | Validated URL format |
| `short_code` | `VARCHAR(10)` | `UNIQUE`, `db_index=True` |
| `click_count` | `INTEGER` | `CHECK >= 0`, default 0 |
| `created_at` | `TIMESTAMPTZ` | `auto_now_add=True` |

---

## 🚀 Quick Start

### Prerequisites

- [Docker](https://www.docker.com/get-started) & Docker Compose
- OR Python 3.12 + PostgreSQL (for local development)

### Option 1: Docker Compose (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/Thulasinath8055/url-shortener.git
cd url-shortener

# 2. Create environment file
cp .env.example .env

# 3. Start PostgreSQL and Django
docker-compose up -d

# 4. Run migrations
docker-compose exec web python manage.py migrate

# 5. Create a superuser (optional)
docker-compose exec web python manage.py createsuperuser

Visit:
🌐 Landing Page: http://localhost:8000/
📚 Swagger UI: http://localhost:8000/api/schema/swagger-ui/
🔧 Admin Panel: http://localhost:8000/admin/