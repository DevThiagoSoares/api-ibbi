from sqlalchemy.orm import Session
from fastapi import HTTPException
from api.repositories.purchase_repository import PurchaseRepository

class PurchaseService:
    def __init__(self, db: Session):
        self.purchase_repo = PurchaseRepository(db)

    def finalize_purchase(self, user_id: int):
        shopping_cart = self.purchase_repo.get_shopping_cart_by_user_id(user_id)
        
        if not shopping_cart:
            raise HTTPException(status_code=404, detail="Carrinho não encontrado")
        
        finished_purchase = self.purchase_repo.create_finished_purchase(user_id, shopping_cart.purchases)
        self.purchase_repo.delete_shopping_cart(shopping_cart)
        
        return {"message": "Compra finalizada com sucesso"}