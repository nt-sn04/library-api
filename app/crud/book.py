from typing import List

from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.genre import Genre
from app.models.author import Author
from app.schemas.book import BookCreate, BookUpdate


def get_books(
    db: Session,
    search: str = "",
    author_id: int | None = None,
    genre_id: int | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    offset: int = 0,
    limit: int = 20,
) -> List[Book]:
    q = db.query(Book)

    if search:
        q = q.filter(Book.title.ilike(f"%{search}%"))

    if author_id:
        q = q.filter(Book.author_id == author_id)

    if genre_id:
        q = q.filter(Book.genres.any(Genre.id == genre_id))

    if year_from:
        q = q.filter(Book.published_year >= year_from)

    if year_to:
        q = q.filter(Book.published_year <= year_to)

    return q.offset(offset).limit(limit).all()


def create_book(db: Session, data: BookCreate) -> Book:
    book = Book(
        title=data.title,
        author_id=data.author_id,
        description=data.description,
        isbn=data.isbn,
        published_year=data.published_year,
        pages=data.pages,
    )

    if data.genre_ids:
        genres = db.query(Genre).filter(Genre.id.in_(data.genre_ids)).all()
        book.genres = genres

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


def get_book(db: Session, id: int) -> Book | None:
    return db.query(Book).get(id)


def update_book(db: Session, existing_book: Book, data: BookUpdate) -> Book:
    if data.title is not None:
        existing_book.title = data.title
    if data.description is not None:
        existing_book.description = data.description
    if data.isbn is not None:
        existing_book.isbn = data.isbn
    if data.published_year is not None:
        existing_book.published_year = data.published_year
    if data.pages is not None:
        existing_book.pages = data.pages
    if data.author_id is not None:
        existing_book.author_id = data.author_id
    if data.genre_ids is not None:
        genres = db.query(Genre).filter(Genre.id.in_(data.genre_ids)).all()
        existing_book.genres = genres

    db.add(existing_book)
    db.commit()
    db.refresh(existing_book)

    return existing_book


def delete_book(db: Session, existing_book: Book) -> None:
    db.delete(existing_book)
    db.commit()


def get_books_by_author(
    db: Session, author: Author, skip: int = 0, limit: int = 20
) -> List[Book]:
    return (
        db.query(Book).filter_by(author_id=author.id).offset(skip).limit(limit).all()
    )

def get_books_by_genre(
    db: Session, genre: Genre, skip: int = 0, limit: int = 20
) -> List[Book]:
    return (
        db.query(Book)
        .filter(Book.genres.any(Genre.id == genre.id))
        .offset(skip)
        .limit(limit)
        .all()
    )