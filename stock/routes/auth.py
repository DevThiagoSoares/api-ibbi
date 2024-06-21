from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from shared.security import create_access_token, verify_password, get_password_hash
from shared.dependencies import get_db
from stock.models.user import User
from stock.schemas.user import UserCreate, Token

router = APIRouter(prefix="/api", tags=["auth"])

class AuthRequest(BaseModel):
    email: str
    password: str

@router.post("/auth", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(auth_request: AuthRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == auth_request.email).first()

    if not user or not verify_password(auth_request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/user", response_model=UserCreate)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return user
