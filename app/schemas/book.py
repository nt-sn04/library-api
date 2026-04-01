from typing import List
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.author import AuthorResponse
from app.schemas.genre import GenreResponse


class BookResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    isbn: str | None = None
    published_year: int | None = None
    pages: int | None = None
    author: AuthorResponse
    genres: List[GenreResponse] = []

    model_config = ConfigDict(from_attributes=True)


class BookCreate(BaseModel):
    title: str = Field(max_length=255)
    author_id: int
    genre_ids: List[int] = []
    description: str | None = None
    isbn: str | None = None
    published_year: int | None = Field(None, ge=1000, le=2100)
    pages: int | None = Field(None, gt=0)


class BookUpdate(BaseModel):
    title: str | None = Field(None, max_length=255)
    author_id: int | None = None
    genre_ids: List[int] | None = None
    description: str | None = None
    isbn: str | None = None
    published_year: int | None = Field(None, ge=1000, le=2100)
    pages: int | None = Field(None, gt=0)