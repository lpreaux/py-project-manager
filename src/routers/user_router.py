from fastapi import APIRouter
from sqlmodel import Session

from src.database import engine
from src.servcies import UserService

router = APIRouter(prefix="/users")
service = UserService()

@router.get("/")
async def read_users():
    with Session(engine) as session:
        return service.get_all_users(session)


