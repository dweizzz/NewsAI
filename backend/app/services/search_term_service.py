from sqlalchemy.orm import Session
from ..database.models import SearchTerm
from typing import List

def get_user_search_terms(db: Session, user_id: int) -> List[SearchTerm]:
    """Get all search terms for a specific user."""
    return db.query(SearchTerm)\
        .filter(SearchTerm.user_id == user_id)\
        .order_by(SearchTerm.created_at.desc())\
        .all()

def create_search_term(db: Session, user_id: int, term: str) -> SearchTerm:
    """Create a new search term for a user."""
    db_search_term = SearchTerm(
        term=term,
        user_id=user_id
    )
    
    db.add(db_search_term)
    db.commit()
    db.refresh(db_search_term)
    
    return db_search_term 