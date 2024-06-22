from sqlalchemy.orm import Session
from sqlalchemy import text

class DashboardRepository:

    def get_top_categories(db: Session):
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
        
        return db.execute(query).fetchall()

    def get_recent_sales(db: Session):
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
        
        return db.execute(query).fetchall()

    def get_low_stock_products(db: Session):
        query = text("""
            SELECT 
                id,
                name,
                price,
                quantity
            FROM 
                products
            ORDER BY 
                quantity ASC
            LIMIT 10;
        """)
        
        return db.execute(query).fetchall()

    def get_top_selling_products(db: Session):
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
        
        return db.execute(query).fetchall()