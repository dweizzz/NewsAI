from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database
from typing import List
from ..mongodb.config import get_db
from ..schemas.search_term import SearchTerm, SearchTermCreate
from ..services.search_term_service import get_user_search_terms, create_search_term, delete_search_term
from ..utils.security import get_current_user

router = APIRouter(prefix="/search-terms", tags=["search terms"])

@router.get("/", response_model=List[SearchTerm])
async def read_user_search_terms(
    current_user: dict = Depends(get_current_user),
    db: Database = Depends(get_db)
):
    """
    Get all search terms for the currently logged in user.
    Requires authentication.
    """
    search_terms = get_user_search_terms(db, str(current_user["_id"]))
    return search_terms

@router.post("/", response_model=SearchTerm)
async def create_user_search_term(
    search_term: SearchTermCreate,
    current_user: dict = Depends(get_current_user),
    db: Database = Depends(get_db)
):
    """
    Create a new search term for the currently logged in user.
    Requires authentication.
    """
    return create_search_term(db, str(current_user["_id"]), search_term.term)

@router.delete("/{search_term_id}", response_model=dict)
async def delete_user_search_term(
    search_term_id: str,
    current_user: dict = Depends(get_current_user),
    db: Database = Depends(get_db)
):
    """
    Delete a search term.
    Requires authentication.
    """
    result = delete_search_term(db, search_term_id, str(current_user["_id"]))
    if not result:
        raise HTTPException(status_code=404, detail="Search term not found")
    return {"message": "Search term deleted successfully"}