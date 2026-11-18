from sqlalchemy.orm import Session
from . import models, schemas
from .security import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(models.UserDB).filter(models.UserDB.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.UserDB).filter(models.UserDB.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    # Явный анализ: выводим SQL-запрос (для лабы)
    query = db.query(models.UserDB).offset(skip).limit(limit)
    print(f"SQL Query: {query.statement}")
    return query.all()

def create_user(db: Session, user: schemas.UserCreate):
    try:
        hashed_password = get_password_hash(user.password)
        db_user = models.UserDB(
            name=user.name,
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()  # Транзакция
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()  # Откат при ошибке
        raise e

def update_user_optimistic(db: Session, user_id: int, new_name: str, current_version: int):
    # Оптимистичная блокировка: обновляем только если версия совпадает
    user = db.query(models.UserDB).filter(models.UserDB.id == user_id).first()
    if not user:
        return None
    
    if user.version != current_version:
        raise Exception("Конфликт версий: данные были изменены другим пользователем")
    
    user.name = new_name
    user.version += 1
    db.commit()
    db.refresh(user)
    return user
