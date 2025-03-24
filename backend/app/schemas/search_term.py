from pydantic import BaseModel
from datetime import datetime

class SearchTermBase(BaseModel):
    term: str

class SearchTermCreate(SearchTermBase):
    pass

class SearchTerm(SearchTermBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True 