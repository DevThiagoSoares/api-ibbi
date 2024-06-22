from pydantic import BaseModel
from pydantic import BaseModel
from typing import List

class ShoppingCartItem(BaseModel):
    product_id: int
    quantity: int

class ShoppingCartResponse(BaseModel):
    user_id: int
    items: List[ShoppingCartItem]


class AddToCartRequest(BaseModel):
    product_id: int
    quantidade: int

class UpdateCartRequest(BaseModel):
   product_id: int
   quantity: int
