from sqlmodel import Session

from src.models import UserCreate, UserUpdate
from src.repositories import UserRepository
from src.models import User


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_all_users(self, db: Session):
        return self.repository.get_all_users(db)
    
    def get_user_by_id(self, user_id: int, db: Session):
        return self.repository.get_user_by_id(db, user_id)
    
    def create_user(self, user_data: UserCreate, db: Session):
        user = User(**user_data.model_dump(exclude={"password_confirm"}))
        return self.repository.create_user(db, user)
    
    def update_user(self, user_id: int, user_data: UserUpdate, db: Session):
        user = self.repository.get_user_by_id(db, user_id)
        if user:
            update_data = user_data.model_dump(exclude={"password_confirm"}, exclude_unset=True)
            for key, value in update_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            return self.repository.update_user(db, user)
        return None
    
    def delete_user(self, user_id: int, db: Session):
        return self.repository.delete_user(db, user_id)