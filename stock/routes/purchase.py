from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from stock.models.finished_purchase import FinishedPurchase
from stock.models.shopping_cart import ShoppingCart
from stock.models.user import User
from shared.dependencies import get_db
from shared.security import get_current_user

router = APIRouter(prefix="/api", tags=["purchase"])


@router.post("/purchase/finalize")
async def finalizar_compra(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user

    # Verifica se há um carrinho ativo para o usuário
    shopping_cart = (
        db.query(ShoppingCart)
        .filter(ShoppingCart.user_id == user_id)
        .options(selectinload(ShoppingCart.purchases))
        .first()
    )

    if not shopping_cart:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Carrinho não encontrado")

    # Cria uma entrada em FinishedPurchase com base nas compras atuais no carrinho
    finished_purchase = FinishedPurchase(user_id=user_id, purchases=shopping_cart.purchases)
    db.add(finished_purchase)
    db.commit()

    # Limpa o carrinho após finalizar a compra
    db.delete(shopping_cart)
    db.commit()

    return {"message": "Compra finalizada com sucesso"}