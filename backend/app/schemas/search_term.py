from pydantic import BaseModel, Field, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from datetime import datetime
from typing import Optional, Any, Dict, Annotated
from bson import ObjectId

# More robust ObjectId handling for Pydantic v2
class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectID")
        return str(v)

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        return core_schema.with_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.str_schema(),
        )

# For Pydantic V2 compatibility
class SearchTermBase(BaseModel):
    term: str

class SearchTermCreate(SearchTermBase):
    pass

class SearchTerm(SearchTermBase):
    id: PyObjectId = Field(default=None, alias="_id")
    user_id: str
    created_at: datetime

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "_id": "60d5ec9af3c56a289b12345",
                "term": "artificial intelligence",
                "user_id": "60d5ec9af3c56a289b54321",
                "created_at": "2023-01-01T00:00:00.000Z"
            }
        }