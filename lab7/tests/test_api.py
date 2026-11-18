import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base
from app import models

# Создаем тестовую базу данных в памяти (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Переопределяем зависимость get_db, чтобы использовалась тестовая БД
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# --- ИНТЕГРАЦИОННЫЕ ТЕСТЫ ---

def test_create_user():
    response = client.post("/users", json={"name": "Test User", "email": "test@example.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert "id" in data

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_create_user_invalid_email():
    response = client.post("/users", json={"name": "Bad Email", "email": "not-an-email"})
    assert response.status_code == 422  # Ошибка валидации

def test_create_user_short_name():
    response = client.post("/users", json={"name": "A", "email": "short@example.com"})
    assert response.status_code == 422  # Ошибка валидации
