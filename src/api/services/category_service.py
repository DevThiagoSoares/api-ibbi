from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.api.models.category import Category
from src.api.schemas.category import CategoryRequest
from src.api.repositories.category_repository import CategoryRepository

class CategoryService:
    
    @staticmethod
    def get_all(db: Session):
        return CategoryRepository.get_all(db)

    @staticmethod
    def get_by_id(db: Session, category_id: int):
        category = CategoryRepository.get_by_id(db, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    @staticmethod
    def create(db: Session, category_request: CategoryRequest):
        category = Category(**category_request.dict())
        return CategoryRepository.create(db, category)

    @staticmethod
    def delete(db: Session, category_id: int):
        category = CategoryRepository.get_by_id(db, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        if CategoryRepository.has_linked_products(db, category_id):
            raise HTTPException(status_code=400, detail="Category has linked products, cannot delete.")
        CategoryRepository.delete(db, category)
        return category

    @staticmethod
    def update(db: Session, category_id: int, category_request: CategoryRequest):
        category = CategoryRepository.get_by_id(db, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        updates = category_request.dict(exclude_unset=True)
        return CategoryRepository.update(db, category, updates)
