from datetime import datetime
from typing import Dict, Any
from pymongo.database import Database

# User model
class UserModel:
    collection_name = "users"

    @staticmethod
    def create_indexes(db):
        db[UserModel.collection_name].create_index("email", unique=True)
        db[UserModel.collection_name].create_index("username", unique=True)

    @staticmethod
    def to_document(email: str, username: str, hashed_password: str) -> Dict[str, Any]:
        now = datetime.utcnow()
        return {
            "email": email,
            "username": username,
            "hashed_password": hashed_password,
            "is_active": True,
            "is_superuser": False,
            "created_at": now,
            "updated_at": now
        }

# SearchTerm model
class SearchTermModel:
    collection_name = "search_terms"

    @staticmethod
    def create_indexes(cls, db: Database):
        """Create necessary indexes for the SearchTerm collection."""
        db[cls.collection_name].create_index(
            [("user_id", 1), ("term", 1)],
            unique=True
        )

    @staticmethod
    def to_document(term: str, user_id: str) -> Dict[str, Any]:
        return {
            "term": term,
            "user_id": user_id,
            "created_at": datetime.utcnow()
        }