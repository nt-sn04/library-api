from typing import Annotated, List

from fastapi import APIRouter, Query, Path, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.book import BookResponse
from app.crud.book import get_books_by_genre
from app.dependencies import get_db
from app.crud.genre import (
    get_genres,
    create_genre,
    get_genre,
    get_genre_by_name,
    update_genre,
    delete_genre,
)
from app.schemas.genre import GenreResponse, GenreCreate, GenreUpdate

router = APIRouter(tags=["genres"])


@router.get("/api/genres", response_model=List[GenreResponse], status_code=200)
async def get_genres_view(
    db: Annotated[Session, Depends(get_db)],
    search: Annotated[str, Query()] = "",
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
):
    return get_genres(db, search, skip, limit)


@router.post("/api/genres", response_model=GenreResponse, status_code=201)
async def create_genre_view(
    db: Annotated[Session, Depends(get_db)], data: GenreCreate
):
    existing = get_genre_by_name(db, data.name)
    if existing:
        raise HTTPException(status_code=400, detail="Genre with this name already exists.")

    genre = create_genre(db, data)

    return genre


@router.get("/api/genres/{id}", response_model=GenreResponse)
async def get_genre_view(
    id: Annotated[int, Path(ge=0)], db: Annotated[Session, Depends(get_db)]
):
    genre = get_genre(db, id)
    if genre:
        return genre
    else:
        raise HTTPException(status_code=404, detail="genre not found.")


@router.patch("/api/genres/{id}", response_model=GenreResponse)
async def update_genre_view(
    id: Annotated[int, Path(ge=0)],
    db: Annotated[Session, Depends(get_db)],
    data: GenreUpdate,
):
    existing_genre = get_genre(db, id)
    if existing_genre is None:
        raise HTTPException(status_code=404, detail="genre not found.")

    if data.name:
        duplicate = get_genre_by_name(db, data.name)
        if duplicate and duplicate.id != id:
            raise HTTPException(status_code=400, detail="Genre with this name already exists.")

    genre = update_genre(db, existing_genre, data)

    return GenreResponse(
        id=genre.id,
        name=genre.name,
        description=genre.description,
    )


@router.delete("/api/genres/{id}")
async def delete_genre_view(
    id: Annotated[int, Path(ge=0)], db: Annotated[Session, Depends(get_db)]
):
    existing_genre = get_genre(db, id)
    if existing_genre is None:
        raise HTTPException(status_code=404, detail="genre not found.")

    delete_genre(db, existing_genre)

    return {"message": "genre deleted."}

@router.get("/api/genres/{id}/books", response_model=List[BookResponse], status_code=200)
async def get_genre_books_view(
    id: Annotated[int, Path(ge=0)],
    db: Annotated[Session, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
):
    genre = get_genre(db, id)
    if genre is None:
        raise HTTPException(status_code=404, detail="genre not found.")

    return get_books_by_genre(db, genre, skip, limit)