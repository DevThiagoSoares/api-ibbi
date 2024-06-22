from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.shared.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Relacionamento com o carrinho de compras
    shopping_cart = relationship("ShoppingCart", back_populates="user")

    def __repr__(self):
        return f'<User(username={self.username}, email={self.email})>'
