from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.models import UserCreate, UserUpdate, UserResponse
from src.database import get_session
from src.servcies import UserService

router = APIRouter(prefix="/users", tags=["users"])
service = UserService()

@router.get("/", response_model=list[UserResponse])
async def read_users(db: Session = Depends(get_session)):
    """Get all users"""
    return service.get_all_users(db)

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: Session = Depends(get_session)):
    """Get a specific user by ID"""
    user = service.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user_data: UserCreate, db: Session = Depends(get_session)):
    """Create a new user"""
    try:
        return service.create_user(user_data, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_session)):
    """Update an existing user"""
    try:
        updated_user = service.update_user(user_id, user_data, db)
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_session)):
    """Delete a user"""
    deleted = service.delete_user(user_id, db)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
