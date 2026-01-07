from sqlmodel import Session

from src.repositories.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.repository = UserRepository()


    def get_all_users(self, db: Session):
        return self.repository.get_all_users(db)