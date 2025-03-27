from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId

# Custom Pydantic field for ObjectId
class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectID")
        return str(v)

# Search Term Schemas
class SearchTermBase(BaseModel):
    term: str

class SearchTermCreate(SearchTermBase):
    pass

class SearchTerm(SearchTermBase):
    id: PyObjectId = Field(alias="_id")
    user_id: str
    created_at: datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "_id": "60d5ec9af3c56a289b12345",
                "term": "artificial intelligence",
                "user_id": "60d5ec9af3c56a289b54321",
                "created_at": "2023-01-01T00:00:00.000Z"
            }
        }