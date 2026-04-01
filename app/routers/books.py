from typing import Annotated, List

from fastapi import APIRouter, Query, Path, HTTPException, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.crud.book import (
    get_books,
    create_book,
    get_book,
    update_book,
    delete_book,
    get_books_by_author,
)
from app.crud.author import get_author
from app.crud.genre import get_genre
from app.schemas.book import BookResponse, BookCreate, BookUpdate

router = APIRouter(tags=["books"])


@router.get("/api/books", response_model=List[BookResponse], status_code=200)
async def get_books_view(
    db: Annotated[Session, Depends(get_db)],
    search: Annotated[str, Query()] = "",
    author_id: Annotated[int | None, Query()] = None,
    genre_id: Annotated[int | None, Query()] = None,
    year_from: Annotated[int | None, Query()] = None,
    year_to: Annotated[int | None, Query()] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
):
    return get_books(db, search, author_id, genre_id, year_from, year_to, skip, limit)


@router.post("/api/books", response_model=BookResponse, status_code=201)
async def create_book_view(
    db: Annotated[Session, Depends(get_db)], data: BookCreate
):
    author = get_author(db, data.author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="author not found.")

    if data.genre_ids:
        for genre_id in data.genre_ids:
            genre = get_genre(db, genre_id)
            if genre is None:
                raise HTTPException(status_code=404, detail=f"genre {genre_id} not found.")

    book = create_book(db, data)

    return book


@router.get("/api/books/{id}", response_model=BookResponse)
async def get_book_view(
    id: Annotated[int, Path(ge=1)], db: Annotated[Session, Depends(get_db)]
):
    book = get_book(db, id)
    if book is None:
        raise HTTPException(status_code=404, detail="book not found.")

    return book


@router.patch("/api/books/{id}", response_model=BookResponse)
async def update_book_view(
    id: Annotated[int, Path(ge=1)],
    db: Annotated[Session, Depends(get_db)],
    data: BookUpdate,
):
    existing_book = get_book(db, id)
    if existing_book is None:
        raise HTTPException(status_code=404, detail="book not found.")

    if data.author_id:
        author = get_author(db, data.author_id)
        if author is None:
            raise HTTPException(status_code=404, detail="author not found.")

    if data.genre_ids:
        for genre_id in data.genre_ids:
            genre = get_genre(db, genre_id)
            if genre is None:
                raise HTTPException(status_code=404, detail=f"genre {genre_id} not found.")

    return update_book(db, existing_book, data)


@router.delete("/api/books/{id}")
async def delete_book_view(
    id: Annotated[int, Path(ge=1)], db: Annotated[Session, Depends(get_db)]
):
    existing_book = get_book(db, id)
    if existing_book is None:
        raise HTTPException(status_code=404, detail="book not found.")

    delete_book(db, existing_book)

    return {"message": "book deleted."}


@router.get("/api/authors/{id}/books", response_model=List[BookResponse], status_code=200)
async def get_author_books_view(
    id: Annotated[int, Path(ge=1)],
    db: Annotated[Session, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
):
    author = get_author(db, id)
    if author is None:
        raise HTTPException(status_code=404, detail="author not found.")

    return get_books_by_author(db, author, skip, limit)