from pydantic import BaseModel

class TopCategory(BaseModel):
    category_name: str
    total_quantity: int

class RecentSale(BaseModel):
    product_name: str
    quantity: int
    date_time: str
    user_name: str
    price: float
    total_price: float

class TopSellingProducts(BaseModel):
    product_name: str
    total_quantity: int
