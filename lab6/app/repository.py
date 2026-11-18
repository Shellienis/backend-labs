from sqlalchemy.orm import Session
from . import models, schemas
from .security import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(models.UserDB).filter(models.UserDB.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.UserDB).filter(models.UserDB.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserDB).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.UserDB(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
