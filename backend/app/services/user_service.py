from pymongo.database import Database
from bson import ObjectId
from fastapi import HTTPException
from ..utils.security import get_password_hash, verify_password
from ..mongodb.models import UserModel

def get_user_by_email(db: Database, email: str):
    """Get a user by email."""
    return db[UserModel.collection_name].find_one({"email": email})

def get_user_by_username(db: Database, username: str):
    """Get a user by username."""
    return db[UserModel.collection_name].find_one({"username": username})

def get_user_by_id(db: Database, user_id: str):
    """Get a user by id."""
    return db[UserModel.collection_name].find_one({"_id": ObjectId(user_id)})

def create_user(db: Database, email: str, username: str, password: str):
    """Create a new user."""
    # Check if email already exists
    if get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username already exists
    if get_user_by_username(db, username):
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create new user
    hashed_password = get_password_hash(password)
    user_data = UserModel.to_document(
        email=email,
        username=username,
        hashed_password=hashed_password
    )
    
    result = db[UserModel.collection_name].insert_one(user_data)
    user_data["_id"] = result.inserted_id
    
    return user_data

def authenticate_user(db: Database, email: str, password: str):
    """Authenticate a user."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user