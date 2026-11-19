import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from app.main import app, get_db
from app.database import Base
from app import models

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@db:5432/mydb")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

TEST_USER = {
    "name": "Test User",
    "email": "test@example.com",
    "password": "secret123"
}

def test_create_user():
    db = TestingSessionLocal()
    db.query(models.UserDB).delete()
    db.commit()
    db.close()

    response = client.post("/register", json=TEST_USER)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert "id" in data

def test_login():
    response = client.post("/token", data={"username": TEST_USER["email"], "password": TEST_USER["password"]})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_profile():
    response = client.post("/token", data={"username": TEST_USER["email"], "password": TEST_USER["password"]})
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == TEST_USER["email"]

def test_request_id_header():
    response = client.get("/docs")
    assert "X-Request-ID" in response.headers
