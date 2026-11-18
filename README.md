Backend Labs (Python + FastAPI + Docker)

Репозиторий с лабораторными работами по backend-разработке.

Стек технологий:
Язык: Python 3.12
Фреймворк: FastAPI
База данных: PostgreSQL
ORM: SQLAlchemy
Контейнеризация: Docker, Docker Compose
Веб-сервер: Nginx (reverse proxy)
Тестирование: Pytest, HTTPX
Аутентификация: JWT (JSON Web Tokens)

Список лабораторных работ:
lab1 — Базовый HTTP-сервер и Docker.
lab2 — REST API (CRUD) для сущности User.
lab3 — Валидация данных и обработка ошибок.
lab4 — Чистая архитектура (Handler/Service/Repository) и подключение к БД.
lab5 — Автоматическое тестирование (покрытие 90%).
lab6 — Аутентификация (JWT) и профили пользователей.
lab7 — Транзакции, оптимистичные блокировки и индексы.
lab8 — Nginx как reverse proxy, статика и HTTPS.

Как запустить любую лабораторную:
1. Перейдите в папку с нужной лабораторной:
   cd labX
   (где X — номер лабораторной от 1 до 8)

2. Запустите контейнеры:
   docker compose up --build

3. Приложение будет доступно по адресу:
   Для lab1 - lab7: http://localhost:8000/docs
   Для lab8: http://localhost/docs (через Nginx)

Как запустить тесты (для lab5):
В папке lab5 выполните:
docker compose run --rm web pytest --cov=app tests/

Примечания:
Для работы необходим установленный Docker Desktop.
В lab8 для HTTPS используется самоподписанный сертификат (браузер может выдать предупреждение).