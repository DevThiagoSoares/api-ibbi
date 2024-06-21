from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from shared.database import Base

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Numeric, nullable=False)
    quantity = Column(Integer, nullable=False)
    description = Column(String(150), nullable=False)
    image = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship('Category', back_populates='products')  # Correção aqui

    def __repr__(self):
        return f'<Product(name={self.name}, price={self.price}, quantity={self.quantity})>'
