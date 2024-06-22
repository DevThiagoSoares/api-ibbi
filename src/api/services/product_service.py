from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.api.repositories.product_repository import ProductRepository
from src.api.schemas.product import ProductRequest

class ProductService:
    def __init__(self, db: Session):
        self.product_repo = ProductRepository(db)

    def get_all_products(self):
        return self.product_repo.get_all_products()

    def get_product_by_id(self, id: int):
        product = self.product_repo.get_product_by_id(id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    def create_product(self, product_request: ProductRequest):
        category = self.product_repo.get_category_by_id(product_request.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return self.product_repo.create_product(product_request.dict())

    def delete_product(self, id: int):
        product = self.product_repo.get_product_by_id(id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return self.product_repo.delete_product(id)

    def update_product(self, id: int, product_request: ProductRequest):
        product = self.product_repo.get_product_by_id(id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        category = self.product_repo.get_category_by_id(product_request.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return self.product_repo.update_product(id, product_request.dict(exclude_unset=True))