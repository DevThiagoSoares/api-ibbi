from sqlalchemy.orm import Session
from src.api.repositories.dashboard_repository import DashboardRepository
from src.api.schemas.dashboard import TopCategory, RecentSale, TopSellingProducts

class DashboardService:
    def get_top_categories(db: Session):
        categories = []
        results = DashboardRepository.get_top_categories(db)
        
        for row in results:
            category_name = row[0]
            total_quantity = row[1]
            if total_quantity is not None:
                categories.append(TopCategory(category_name=category_name, total_quantity=int(total_quantity)))
            else:
                categories.append(TopCategory(category_name=category_name, total_quantity=0))
        
        return categories

    def get_recent_sales(db: Session):
        recent_sales = []
        results =  DashboardRepository.get_recent_sales(db)

        for row in results:
            recent_sales.append(RecentSale(
                product_name=row[0],
                quantity=row[1],
                date_time = row[2].strftime("%d/%m/%Y %H:%Mh"),
                user_name=row[3],
                price=row[4],
                total_price=row[5]
            ))

        return recent_sales

    def get_low_stock_products(db: Session):
        results =  DashboardRepository.get_low_stock_products(db)
        low_stock_products = [
            {"id": row[0], "name": row[1], "price": row[2], "quantity": row[3]} for row in results
        ]
        return low_stock_products

    def get_top_selling_products(db: Session):
        results =  DashboardRepository.get_top_selling_products(db)
        top_selling_products = [
            TopSellingProducts(
                product_name=row[0],
                total_quantity=int(row[1])
            ) for row in results
        ]
        return top_selling_products