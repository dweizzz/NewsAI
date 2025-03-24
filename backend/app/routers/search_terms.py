from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database.config import get_db
from ..schemas.search_term import SearchTerm, SearchTermCreate
from ..services.search_term_service import get_user_search_terms, create_search_term
from ..utils.security import get_current_user
from ..database.models import User

router = APIRouter(prefix="/search-terms", tags=["search terms"])

@router.get("/", response_model=List[SearchTerm])
async def read_user_search_terms(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all search terms for the currently logged in user.
    Requires authentication.
    """
    search_terms = get_user_search_terms(db, current_user.id)
    return search_terms

@router.post("/", response_model=SearchTerm)
async def create_user_search_term(
    search_term: SearchTermCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new search term for the currently logged in user.
    Requires authentication.
    """
    return create_search_term(db, current_user.id, search_term.term) 