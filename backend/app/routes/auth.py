from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import get_db, User
from app.services.auth_service import auth_service
from pydantic import BaseModel, EmailStr

router = APIRouter()

class UserAuth(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserAuth, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = auth_service.get_password_hash(user_data.password)
    new_user = User(email=user_data.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@router.post("/login", response_model=Token)
def login(user_data: UserAuth, db: Session = Depends(get_db)):
    print(f"Login attempt for: {user_data.email}")
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail=f"User not found: {user_data.email}")
    
    verified = auth_service.verify_password(user_data.password, user.hashed_password)
    
    if not verified:
        raise HTTPException(status_code=401, detail=f"Password mismatch for {user_data.email}. Stored hash: {user.hashed_password[:10]}...")
    
    access_token = auth_service.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
