from typing import List, Dict, Union
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from shared.dependencies import get_db
from stock.models.category import Category
from stock.models.product import Product

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

class TopCategory(BaseModel):
    category_name: str
    total_quantity: int
    
class RecentSale(BaseModel):
    product_name: str
    quantity: int
    date_time: str  # Você pode ajustar o tipo de data conforme necessário
    user_name: str
    price: float
    total_price: float

class TopSellingProducts(BaseModel):
    product_name: str
    total_quantity: int
    

@router.get("/top-categories", response_model=List[TopCategory])
def get_top_categories(db: Session = Depends(get_db)):
    query = text("""
               WITH category_sales AS (
                SELECT 
                    c.name AS category_name,
                    SUM(pur.quantity) AS total_quantity
                FROM 
                    purchases pur
                JOIN 
                    products p ON pur.product_id = p.id
                JOIN 
                    categories c ON p.category_id = c.id
                WHERE 
                    pur.finished_purchase_id IS NOT NULL
                GROUP BY 
                    c.name
            ),
            top_categories AS (
                SELECT 
                    category_name,
                    total_quantity
                FROM 
                    category_sales
                ORDER BY 
                    total_quantity DESC
                LIMIT 3
            ),
            other_categories AS (
                SELECT 
                    'Outras' AS category_name,
                    SUM(total_quantity) AS total_quantity
                FROM 
                    (
                        SELECT 
                            c.name AS category_name,
                            SUM(pur.quantity) AS total_quantity
                        FROM 
                            purchases pur
                        JOIN 
                            products p ON pur.product_id = p.id
                        JOIN 
                            categories c ON p.category_id = c.id
                        WHERE 
                            pur.finished_purchase_id IS NOT NULL
                            AND c.name NOT IN (
                                SELECT category_name FROM top_categories
                            )
                        GROUP BY 
                            c.name
                    ) AS others
            )
            SELECT * FROM top_categories
            UNION ALL
            SELECT * FROM other_categories;
    """)
    
    results = db.execute(query)
    print("======>",results)

    # # Transformando os resultados em uma lista de objetos TopCategory
    categories = []
    for row in results:
        category_name = row[0]
        total_quantity = row[1]
        if total_quantity is not None:
            categories.append(TopCategory(category_name=category_name, total_quantity=int(total_quantity)))
        else:
            categories.append(TopCategory(category_name=category_name, total_quantity=0))  # Ou outro valor padrão que faça sentido
    
    return categories



@router.get("/recent-sales", response_model=List[RecentSale])
def get_recent_sales(db: Session = Depends(get_db)):
    query = text("""
        SELECT 
            p.name AS product_name,
            pur.quantity AS quantity,
            pur.date_time AS date_time,
            u.username AS user_name,
            p.price AS price,
            (p.price * pur.quantity) AS total_price
        FROM 
            finished_purchases fp
        JOIN 
            purchases pur ON fp.id = pur.finished_purchase_id
        JOIN 
            products p ON pur.product_id = p.id
        JOIN 
            users u ON fp.user_id = u.id
        ORDER BY 
            pur.date_time DESC
        LIMIT 4;
    """)
    
    results = db.execute(query)
    recent_sales = [RecentSale(
        product_name=row[0],
        quantity=row[1],
        date_time=str(row[2]),
        user_name=row[3],
        price=row[4],
        total_price=row[5]
    ) for row in results]
    
    return recent_sales


@router.get("/low-stock-products", response_model=List[dict])
def get_low_stock_products(db: Session = Depends(get_db)):
    query = db.query(Product).order_by(Product.quantity.asc()).limit(10).all()
    low_stock_products = [{"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity} for product in query]
    return low_stock_products

@router.get("/top-selling-products", response_model=List[TopSellingProducts])
def get_top_selling_products(db: Session = Depends(get_db)):
    query = text("""
        SELECT 
            p.name AS product_name,
            SUM(pur.quantity) AS total_quantity
        FROM 
            purchases pur
        JOIN 
            products p ON pur.product_id = p.id
        WHERE 
            pur.finished_purchase_id IS NOT NULL
        GROUP BY 
            p.name
        ORDER BY 
            total_quantity DESC
        LIMIT 10;
    """)
    
    results = db.execute(query)
    top_selling_products = [
        TopSellingProducts(
            product_name=row[0],
            total_quantity=int(row[1])
        ) for row in results
    ]
    return top_selling_products