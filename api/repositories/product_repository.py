from sqlalchemy.orm import Session
from api.models.product import Product
from api.models.category import Category

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_products(self):
        return self.db.query(Product).all()

    def get_product_by_id(self, id: int):
        return self.db.query(Product).filter(Product.id == id).first()

    def create_product(self, product_data: dict):
        product = Product(**product_data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, id: int):
        product = self.get_product_by_id(id)
        if product:
            self.db.delete(product)
            self.db.commit()
        return product

    def update_product(self, id: int, product_data: dict):
        product = self.get_product_by_id(id)
        if product:
            for key, value in product_data.items():
                setattr(product, key, value)
            self.db.commit()
            self.db.refresh(product)
        return product

    def get_category_by_id(self, category_id: int):
        return self.db.query(Category).filter(Category.id == category_id).first()