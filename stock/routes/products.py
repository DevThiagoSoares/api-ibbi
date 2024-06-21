from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from shared.dependencies import get_db
from stock.schemas.product import ProductRequest, ProductResponse
from stock.schemas.purchase import PurchaseResponse
from stock.schemas.shopping_cart import ShoppingCartResponse

from stock.models.product import Product
from stock.models.category import Category
from stock.models.shopping_cart import ShoppingCart
from stock.models.purchase import Purchase
from stock.models.user import User
from shared.security import get_current_user

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("", response_model=List[ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@router.get("/{id}", response_model=ProductResponse)
async def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("", response_model=ProductResponse, status_code=201)
async def create_product(product_request: ProductRequest, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == product_request.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    product = Product(**product_request.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{id}", response_model=ProductResponse)
async def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return product

@router.patch("/{id}", response_model=ProductResponse)
async def update_product(id: int, product_request: ProductRequest, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    category = db.query(Category).filter(Category.id == product_request.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in product_request.dict(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


