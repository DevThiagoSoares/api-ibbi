from datetime import datetime
from sqlalchemy.orm import Session, selectinload
from src.api.models.shopping_cart import ShoppingCart
from src.api.models.finished_purchase import FinishedPurchase

class PurchaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_shopping_cart_by_user_id(self, user_id: int):
        return (
            self.db.query(ShoppingCart)
            .filter(ShoppingCart.user_id == user_id)
            .options(selectinload(ShoppingCart.purchases))
            .first()
        )

    def create_finished_purchase(self, user_id: int, purchases: list, date_time: datetime):
        finished_purchase = FinishedPurchase(user_id=user_id, purchases=purchases)
        for purchase in purchases:
            purchase.date_time = date_time
        self.db.add(finished_purchase)
        self.db.commit()
        return finished_purchase

    def delete_shopping_cart(self, shopping_cart: ShoppingCart):
        self.db.delete(shopping_cart)
        self.db.commit()