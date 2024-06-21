
from pydantic import BaseModel
from typing import List, Dict
from stock.schemas.product import ProductResponse
from pydantic import BaseModel
from typing import List, Optional

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
