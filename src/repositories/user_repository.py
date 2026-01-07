from sqlmodel import Session, select

from src.models import User


class UserRepository:
    
    def create_user(self, db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_all_users(self, db: Session) -> list[User]:
        return db.exec(select(User)).all()

    def get_user_by_id(self, db: Session, user_id: int) -> User | None:
        return db.get(User, user_id)

    def update_user(self, db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def delete_user(self, db: Session, user_id: int) -> bool:
        user = db.get(User, user_id)
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
