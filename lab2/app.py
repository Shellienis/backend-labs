from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI(title="User API", description="CRUD API для лабораторной работы 2")

# Модель данных (схема, как выглядит пользователь)
class User(BaseModel):
    id: int
    name: str
    email: str

# Наша "база данных" в памяти (пока без реальной БД)
users_db = []

# 1. GET: Получить всех пользователей
@app.get("/users", response_model=List[User])
def get_users():
    return users_db

# 2. POST: Создать нового пользователя
@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    # Проверка, что такого ID еще нет
    for u in users_db:
        if u.id == user.id:
            raise HTTPException(status_code=400, detail="User with this ID already exists")
    users_db.append(user)
    return user

# 3. PUT: Обновить пользователя по ID
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    for i, u in enumerate(users_db):
        if u.id == user_id:
            users_db[i] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

# 4. DELETE: Удалить пользователя по ID
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    global users_db
    for i, u in enumerate(users_db):
        if u.id == user_id:
            users_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="User not found")
