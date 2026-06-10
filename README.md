# 📝 Simple Flask Todo API

Backend для Todo-приложения на Flask + PostgreSQL (Supabase).  
Поддерживает CRUD-операции и используется вместе с фронтендом (React).

---

## ⚙️ Технологии

- Python 3.10+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate (Alembic)
- PostgreSQL (Supabase)
- Flask-CORS

---

## 🚀 Как запустить проект

### 1. Клонировать репозиторий

```bash
git clone <repo-url>
cd simple_flask_todo
flask run --debug - старт с перезапуском при измененнии
flask db upgrade - накатить модель