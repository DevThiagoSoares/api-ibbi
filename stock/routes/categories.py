from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from stock.models.category import Category
from stock.schemas.category import CategoryRequest, CategoryResponse

router = APIRouter(prefix="/api/categories", tags=["categories"])

@router.get(path="", response_model=List[CategoryResponse])
async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories

@router.get(path="/{id}", response_model=CategoryResponse)
async def get_category(id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post(path="", response_model=CategoryResponse, status_code=201)
async def create_category(category_request: CategoryRequest, db: Session = Depends(get_db)):
    category = Category(**category_request.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.delete(path="/{id}", response_model=CategoryResponse)
async def delete_category(id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return category

@router.patch(path="/{id}", response_model=CategoryResponse)
async def update_category(id: int, category_request: CategoryRequest, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category_request.dict(exclude_unset=True).items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category