# stock/models/purchase.py

from sqlalchemy import Column, Integer, ForeignKey, Time, DateTime
from sqlalchemy.orm import relationship
from shared.database import Base

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    shopping_cart_id = Column(Integer, ForeignKey('shopping_carts.id'))
    date_time = Column(DateTime, nullable=True)
    finished_purchase_id = Column(Integer, ForeignKey('finished_purchases.id'))

    # Relacionamento de volta com o carrinho de compras
    shopping_cart = relationship("ShoppingCart", back_populates="purchases")

    # Relacionamento com a compra finalizada
    finished_purchase = relationship("FinishedPurchase", back_populates="purchases")

    # Relacionamento com o produto
    product = relationship("Product")

    def __repr__(self):
        return f'<Purchase(product_id={self.product_id}, quantity={self.quantity})>'
