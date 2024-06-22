from pydantic import BaseModel
from api.schemas.category import CategoryResponse

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    description: str
    image: str
    category_id: int
    category: CategoryResponse

    class Config:
        from_attributes = True


class ProductRequest(BaseModel):
    name: str
    price: float
    quantity: int
    description: str
    image: str
    category_id: int
