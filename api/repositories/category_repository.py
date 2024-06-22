from sqlalchemy.orm import Session
from api.models.category import Category
from api.models.product import Product

class CategoryRepository:
    
    @staticmethod
    def get_all(db: Session):
        return db.query(Category).all()

    @staticmethod
    def get_by_id(db: Session, category_id: int):
        return db.query(Category).filter(Category.id == category_id).first()

    @staticmethod
    def create(db: Session, category: Category):
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def delete(db: Session, category: Category):
        db.delete(category)
        db.commit()

    @staticmethod
    def update(db: Session, category: Category, updates: dict):
        for key, value in updates.items():
            setattr(category, key, value)
        db.commit()
        db.refresh(category)
        return category
 
    @staticmethod
    def has_linked_products(db: Session, category_id: int):
        return db.query(Product).filter(Product.category_id == category_id).first() is not None
