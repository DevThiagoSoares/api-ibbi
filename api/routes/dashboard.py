from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from api.services.dashboard_service import DashboardService
from api.schemas.dashboard import TopCategory, RecentSale, TopSellingProducts

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/top-categories", response_model=List[TopCategory])
def get_top_categories(db: Session = Depends(get_db)):
    return DashboardService.get_top_categories(db)

@router.get("/recent-sales", response_model=List[RecentSale])
def get_recent_sales(db: Session = Depends(get_db)):
    return DashboardService.get_recent_sales(db)

@router.get("/low-stock-products", response_model=List[dict])
def get_low_stock_products(db: Session = Depends(get_db)):
    return DashboardService.get_low_stock_products(db)

@router.get("/top-selling-products", response_model=List[TopSellingProducts])
def get_top_selling_products(db: Session = Depends(get_db)):
    return DashboardService.get_top_selling_products(db)