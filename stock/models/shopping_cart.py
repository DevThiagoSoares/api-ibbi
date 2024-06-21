# stock/models/shopping_cart.py

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
from shared.database import Base
from stock.models.finished_purchase import FinishedPurchase

class ShoppingCart(Base):
    __tablename__ = "shopping_carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relacionamento de volta com o usuário
    user = relationship("User", back_populates="shopping_cart")

    # Relacionamento com as compras (Purchase)
    purchases = relationship("Purchase", back_populates="shopping_cart")

    def finalize_purchase(self):
        # Criar uma entrada em FinishedPurchase com base nas compras atuais no carrinho
        finished_purchase = FinishedPurchase(user_id=self.user_id, purchases=self.purchases)
        return finished_purchase
