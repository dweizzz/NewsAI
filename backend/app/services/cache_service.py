# services/cache_service.py
from pymongo.database import Database
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

def get_cached_insights(db: Database, search_term: str, num_results: int) -> Optional[List[Dict[str, Any]]]:
    """Get cached insights if they exist and are less than 30 minutes old."""
    cache_collection = db["cache"]

    thirty_minutes_ago = datetime.utcnow() - timedelta(minutes=30)  # Correct

    cache_entry = cache_collection.find_one({
        "search_term": search_term,
        "num_results": num_results,
        "created_at": {"$gt": thirty_minutes_ago}
    })

    if cache_entry:
        return cache_entry["insights"]
    return None

def save_insights_to_cache(db: Database, search_term: str, insights: List[Dict[str, Any]], num_results: int) -> None:
    """Save insights to cache."""
    cache_collection = db["cache"]

    cache_collection.update_one(
        {"search_term": search_term, "num_results": num_results},
        {"$set": {
            "insights": insights,
            "created_at": datetime.utcnow()
        }},
        upsert=True
    )