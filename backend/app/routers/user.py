from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database

from ..mongodb.config import get_db
from ..schemas.auth import UserBase
from ..utils.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserBase)
async def get_user_me(current_user: dict = Depends(get_current_user)):
    """Get current user information."""
    return current_user