from sqlmodel import Session
from fastapi import Depends

from src.config import get_password_hasher, PasswordHasher
from src.models import UserCreate, UserUpdate
from src.repositories import UserRepository
from src.models import User


class UserService:
    def __init__(self, pwd_hasher: PasswordHasher):
        self.repository = UserRepository()
        self.pwd_hasher = pwd_hasher

    def get_all_users(self, db: Session):
        return self.repository.get_all_users(db)
    
    def get_user_by_id(self, user_id: int, db: Session):
        return self.repository.get_user_by_id(db, user_id)
    
    def create_user(self, user_data: UserCreate, db: Session):
        user = User(**user_data.model_dump(exclude={"password_confirm"}))
        user.password = self.pwd_hasher.hash(user.password)
        return self.repository.create_user(db, user)
    
    def update_user(self, user_id: int, user_data: UserUpdate, db: Session):
        user = self.repository.get_user_by_id(db, user_id)
        if user:
            if user_data.password:
                user_data.password = self.pwd_hasher.hash(user_data.password)
            update_data = user_data.model_dump(exclude={"password_confirm"}, exclude_unset=True)
            for key, value in update_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            return self.repository.update_user(db, user)
        return None
    
    def delete_user(self, user_id: int, db: Session):
        return self.repository.delete_user(db, user_id)


def get_user_service(pwd_hasher: PasswordHasher = Depends(get_password_hasher)) -> UserService:
    """Dependency function that provides a UserService with injected singleton dependencies"""
    return UserService(pwd_hasher=pwd_hasher)