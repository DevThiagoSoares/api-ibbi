from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.api.schemas.user import AuthRequest, Token, UserCreate
from src.api.services.auth_service import AuthService
from src.shared.dependencies import get_db

router = APIRouter(prefix="/api", tags=["auth"])

@router.post("/auth", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(auth_request: AuthRequest, db: Session = Depends(get_db)):
    token = AuthService.login(auth_request, db)
    return token

@router.post("/user", response_model=UserCreate)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = AuthService.create_user(user, db)
    return new_user
