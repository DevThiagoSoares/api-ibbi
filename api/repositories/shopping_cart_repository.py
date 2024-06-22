from sqlalchemy.orm import Session, selectinload
from api.models.shopping_cart import ShoppingCart
from api.models.product import Product
from api.models.purchase import Purchase
from api.models.user import User

class ShoppingCartRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_product_by_id(self, product_id: int):
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_shopping_cart_by_user_id(self, user_id: int):
        return (
            self.db.query(ShoppingCart)
            .filter(ShoppingCart.user_id == user_id)
            .options(selectinload(ShoppingCart.purchases))
            .first()
        )

    def add_shopping_cart(self, shopping_cart: ShoppingCart):
        self.db.add(shopping_cart)
        self.db.commit()
        self.db.refresh(shopping_cart)
        return shopping_cart

    def update_product_quantity(self, product: Product, quantity: int):
        product.quantity += quantity
        self.db.commit()
    
    def delete_shopping_cart(self, shopping_cart: ShoppingCart):
        self.db.delete(shopping_cart)
        self.db.commit()

    def add_purchase(self, purchase: Purchase):
        self.db.add(purchase)
        self.db.commit()

    def delete_purchase(self, purchase: Purchase):
        self.db.delete(purchase)
        self.db.commit()

    def commit(self):
        self.db.commit()