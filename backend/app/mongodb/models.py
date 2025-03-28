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
    def create_indexes(db: Database):
        """Create necessary indexes for the SearchTerm collection."""
        db[SearchTermModel.collection_name].create_index(
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

# Add to models.py
class CacheModel:
    collection_name = "cache"

    @staticmethod
    def create_indexes(db):
        """Create necessary indexes for the Cache collection."""
        db[CacheModel.collection_name].create_index(
            [("search_term", 1), ("num_results", 1)],
            unique=True
        )
        db[CacheModel.collection_name].create_index(
            "created_at",
            expireAfterSeconds=86400
        )

    @staticmethod
    def to_document(search_term: str, insights: list, num_results: int) -> Dict[str, Any]:
        return {
            "search_term": search_term,
            "insights": insights,
            "num_results": num_results,
            "created_at": datetime
        }