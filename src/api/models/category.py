from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.shared.database import Base

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    products = relationship('Product', back_populates='category')  # Correção aqui

    def __repr__(self):
        return f'<Category(name={self.name}, description={self.description})>'
