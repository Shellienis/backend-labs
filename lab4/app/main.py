from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, repository
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lab 4: Clean Architecture")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users", response_model=list[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return repository.get_users(db, skip=skip, limit=limit)

@app.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return repository.create_user(db=db, user=user)
