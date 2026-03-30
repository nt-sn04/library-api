from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text

from app.database import Base
from app.models.book_genre import book_genres


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    books: Mapped[list["Book"]] = relationship(
        "Book", secondary=book_genres, back_populates="genres"
    )
