# stock/models/finished_purchase.py

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from shared.database import Base

class FinishedPurchase(Base):
    __tablename__ = "finished_purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relacionamento de volta com o usuário
    user = relationship("User")

    # Relacionamento com as compras finalizadas
    purchases = relationship("Purchase", back_populates="finished_purchase")

    def __repr__(self):
        return f'<FinishedPurchase(user_id={self.user_id})>'
