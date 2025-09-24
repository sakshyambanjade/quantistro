from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlalchemy.orm import Session
from app.db import session, models
import logging

logger = logging.getLogger("uvicorn.error")

router = APIRouter()

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

def get_db():
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Create user called with username={user.username}")
    db_user = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    new_user = models.User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info("Reading users from database")
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users
