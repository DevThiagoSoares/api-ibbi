# stock/schemas/purchase.py

from pydantic import BaseModel
from datetime import datetime

class PurchaseResponse(BaseModel):
    id: int
    shopping_cart_id: int
    created_at: datetime

    class Config:
        from_attributes = True
