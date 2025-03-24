from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import ValidationError
from ..database.config import get_db
from ..schemas.auth import Token, UserRegister
from ..services.user_service import authenticate_user, create_user
from ..utils.security import create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=Token)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user."""
    try:
        # Add detailed logging
        print(f"Registration attempt with email: {user_data.email}, username: {user_data.username}")

        user = create_user(
            db=db,
            email=user_data.email,
            username=user_data.username,
            password=user_data.password
        )

        # Create access token
        access_token = create_access_token(
            data={"sub": user.email}
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except ValidationError as e:
        print(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except HTTPException as e:
        print(f"HTTP error: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login for access token."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {"access_token": access_token, "token_type": "bearer"}