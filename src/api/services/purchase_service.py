from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.api.repositories.purchase_repository import PurchaseRepository

class PurchaseService:
    def __init__(self, db: Session):
        self.purchase_repo = PurchaseRepository(db)

    def finalize_purchase(self, user_id: int):
        shopping_cart = self.purchase_repo.get_shopping_cart_by_user_id(user_id)
        
        if not shopping_cart:
            raise HTTPException(status_code=404, detail="Carrinho não encontrado")
        
        current_datetime = datetime.now()  # Obtém a data e hora atuais
        finished_purchase = self.purchase_repo.create_finished_purchase(user_id, shopping_cart.purchases, current_datetime)
        self.purchase_repo.delete_shopping_cart(shopping_cart)
        
        return {"message": "Compra finalizada com sucesso"}