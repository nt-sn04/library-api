from typing import List
from datetime import date

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.author import Author


def get_authors(
    db: Session, search: str = "", offset: int = 0, limit: int = 20
) -> List[Author]:
    q = db.query(Author)

    if search != "":
        pattern = f"%{search}%"

        q = q.filter(
            or_(
                Author.first_name.ilike(pattern),
                Author.last_name.ilike(pattern),
            )
        )

    authors = q.offset(offset).limit(limit).all()

    return authors


def create_author(
    db: Session,
    first_name: str,
    last_name: str,
    bio: str = None,
    born_date: date = None,
) -> Author:
    author = Author(
        first_name=first_name, last_name=last_name, bio=bio, born_date=born_date
    )

    db.add(author)
    db.commit()
    db.refresh(author)

    return author
