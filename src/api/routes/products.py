from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.shared.dependencies import get_db
from src.api.schemas.product import ProductRequest, ProductResponse
from src.api.services.product_service import ProductService

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("", response_model=List[ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.get_all_products()

@router.get("/{id}", response_model=ProductResponse)
async def get_product(id: int, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.get_product_by_id(id)

@router.post("", response_model=ProductResponse, status_code=201)
async def create_product(product_request: ProductRequest, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.create_product(product_request)

@router.delete("/{id}", response_model=ProductResponse)
async def delete_product(id: int, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.delete_product(id)

@router.patch("/{id}", response_model=ProductResponse)
async def update_product(id: int, product_request: ProductRequest, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.update_product(id, product_request)