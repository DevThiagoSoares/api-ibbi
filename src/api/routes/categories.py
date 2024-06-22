from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.shared.dependencies import get_db
from src.api.schemas.category import CategoryRequest, CategoryResponse
from src.api.services.category_service import CategoryService

router = APIRouter(prefix="/api/categories", tags=["categories"])

@router.get(path="", response_model=List[CategoryResponse])
async def get_categories(db: Session = Depends(get_db)):
    return CategoryService.get_all(db)

@router.get(path="/{id}", response_model=CategoryResponse)
async def get_category(id: int, db: Session = Depends(get_db)):
    return CategoryService.get_by_id(db, id)

@router.post(path="", response_model=CategoryResponse, status_code=201)
async def create_category(category_request: CategoryRequest, db: Session = Depends(get_db)):
    return CategoryService.create(db, category_request)

@router.delete(path="/{id}", response_model=CategoryResponse)
async def delete_category(id: int, db: Session = Depends(get_db)):
    return CategoryService.delete(db, id)

@router.patch(path="/{id}", response_model=CategoryResponse)
async def update_category(id: int, category_request: CategoryRequest, db: Session = Depends(get_db)):
    return CategoryService.update(db, id, category_request)
