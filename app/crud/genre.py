from typing import List

from sqlalchemy.orm import Session

from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreUpdate


def get_genres(
    db: Session, search: str = "", offset: int = 0, limit: int = 20
) -> List[Genre]:
    q = db.query(Genre)

    if search != "":
        pattern = f"%{search}%"
        q = q.filter(Genre.name.ilike(pattern))

    genres = q.offset(offset).limit(limit).all()

    return genres


def create_genre(db: Session, data: GenreCreate) -> Genre:
    genre = Genre(
        name=data.name,
        description=data.description,
    )

    db.add(genre)
    db.commit()
    db.refresh(genre)

    return genre


def get_genre(db: Session, id: int) -> Genre | None:
    genre = db.query(Genre).get(id)

    return genre


def get_genre_by_name(db: Session, name: str) -> Genre | None:
    genre = db.query(Genre).filter(Genre.name.ilike(name)).first()

    return genre


def update_genre(db: Session, existing_genre: Genre, data: GenreUpdate) -> Genre:
    existing_genre.name = data.name if data.name else existing_genre.name
    existing_genre.description = (
        data.description if data.description else existing_genre.description
    )

    db.add(existing_genre)
    db.commit()

    return existing_genre


def delete_genre(db: Session, existing_genre: Genre) -> None:
    db.delete(existing_genre)
    db.commit()