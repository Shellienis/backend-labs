from fastapi import FastAPI, HTTPException, status, Request
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="User API Lab 3", description="Валидация и обработка ошибок")

class User(BaseModel):
    id: int = Field(gt=0, description="ID должен быть больше 0")
    name: str = Field(min_length=2, max_length=50, description="Имя от 2 до 50 символов")
    email: EmailStr

    @field_validator('name')
    @classmethod
    def name_must_not_contain_digits(cls, v):
        if any(char.isdigit() for char in v):
            raise ValueError('Имя не должно содержать цифры')
        return v

users_db = []

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {exc}")
    return HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@app.get("/users", response_model=List[User])
def get_users():
    return users_db

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    for u in users_db:
        if u.id == user.id:
            logger.warning(f"Попытка создать пользователя с существующим ID: {user.id}")
            raise HTTPException(status_code=400, detail="Пользователь с таким ID уже существует")
    users_db.append(user)
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    for i, u in enumerate(users_db):
        if u.id == user_id:
            users_db[i] = updated_user
            return updated_user
    logger.warning(f"Попытка обновить несуществующего пользователя ID: {user_id}")
    raise HTTPException(status_code=404, detail="Пользователь не найден")

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    global users_db
    for i, u in enumerate(users_db):
        if u.id == user_id:
            users_db.pop(i)
            return
    logger.warning(f"Попытка удалить несуществующего пользователя ID: {user_id}")
    raise HTTPException(status_code=404, detail="Пользователь не найден")
