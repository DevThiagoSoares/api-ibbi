from sqlalchemy.orm import Session
from src.api.models.user import User

class UserRepository:

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()
