from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from shared.security import get_current_user
from api.models.user import User
from api.schemas.shopping_cart import AddToCartRequest, UpdateCartRequest
from api.services.shopping_cart_service import ShoppingCartService

router = APIRouter(prefix="/api", tags=["shopping_cart"])

@router.post("/shopping-cart")
async def add_product_to_cart(
    request: AddToCartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ShoppingCartService(db)
    return service.add_product_to_cart(current_user, request)

@router.get("/shopping-cart")
async def list_cart_products(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ShoppingCartService(db)
    return service.list_cart_products(current_user)

@router.put("/shopping-cart")
async def update_shopping_cart(
    request: List[UpdateCartRequest],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ShoppingCartService(db)
    return service.update_cart(current_user, request)