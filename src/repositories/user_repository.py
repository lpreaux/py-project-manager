from sqlmodel import Session, select

from ..models import User


class UserRepository:
    def __init__(self):
        pass

    def add_user(self, db: Session, user: User):
        db.add(user)
        db.commit()

    def get_all_users(self, db: Session):
        return db.exec(select(User)).all()

    def get_user(self, db: Session, user_id: int):
        return db.get(User, user_id)

    def update_user(self, db: Session, user: User):
        db.add(user)
        db.commit()

    def delete_user(self, db: Session, user_id: int):
        user = db.get(User, user_id)
        db.delete(user)
        db.commit()
