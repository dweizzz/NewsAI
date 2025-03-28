from pymongo.database import Database
from bson import ObjectId
from typing import List, Dict, Any
from ..mongodb.models import SearchTermModel

def create_search_term(db: Database, term: str, user_id: str) -> Dict[str, Any]:
    """Create a new search term for a user."""
    search_term_data = SearchTermModel.to_document(
        term=term,
        user_id=user_id
    )
    result = db[SearchTermModel.collection_name].insert_one(search_term_data)
    # Convert ObjectId to string before returning
    search_term_data["_id"] = str(result.inserted_id)
    return search_term_data

def get_user_search_terms(db: Database, user_id: str) -> List[Dict[str, Any]]:
    """Get all search terms for a specific user."""
    cursor = db[SearchTermModel.collection_name].find(
        {"user_id": user_id}
    ).sort("created_at", -1)  # -1 for descending order (newest first)

    # Convert ObjectIds to strings in the results
    results = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        results.append(doc)
    return results

def delete_search_term(db: Database, search_term_id: str, user_id: str) -> bool:
    """Delete a search term."""
    result = db[SearchTermModel.collection_name].delete_one({
        "_id": ObjectId(search_term_id),
        "user_id": user_id
    })

    return result.deleted_count > 0

def get_search_term_by_id(db: Database, search_term_id: str) -> Dict[str, Any]:
    """Get a search term by ID."""
    return db[SearchTermModel.collection_name].find_one({"_id": ObjectId(search_term_id)})