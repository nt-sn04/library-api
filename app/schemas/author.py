from typing import List
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AuthorResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    bio: str = ""
    born_date: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class AuthorsResponse(BaseModel):
    limit: int = 20
    skip: int = 0
    search: str = ""
    count: int
    result: List[AuthorResponse]


class Authorcreate(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    bio: str = ""
    born_date: datetime | None = None

    @field_validator("first_name", "last_name")
    @classmethod
    def validate(cls, v: str):
        if not v.strip():
            raise ValueError("Cannot be empty or whitespace only")
        return v.strip()
