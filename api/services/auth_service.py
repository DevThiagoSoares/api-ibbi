from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from api.models.user import User
from api.repositories.user_repository import UserRepository
from api.schemas.user import AuthRequest, UserCreate, Token
from shared.security import create_access_token, verify_password, get_password_hash

class AuthService:

    @staticmethod
    def login(auth_request: AuthRequest, db: Session) -> Token:
        user = UserRepository.get_user_by_email(db, auth_request.email)

        if not user or not verify_password(auth_request.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect login or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    def create_user(user: UserCreate, db: Session) -> UserCreate:
        db_user = UserRepository.get_user_by_email(db, user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        hashed_password = get_password_hash(user.password)
        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return user
