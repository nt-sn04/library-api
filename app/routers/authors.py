from typing import Annotated

from fastapi import APIRouter, Query

from app.dependencies import get_db
from app.crud.author import get_authors, create_author
from app.schemas.author import AuthorsResponse, Authorcreate

router = APIRouter(tags=["authors"])


@router.get("/api/authors", response_model=AuthorsResponse, status_code=200)
async def get_authors_view(
    search: Annotated[str, Query()] = "",
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
):
    db = next(get_db())

    authors = get_authors(db, search, skip, limit)

    response = AuthorsResponse(
        limit=limit, skip=skip, search=search, count=len(authors), result=authors
    )

    return response


@router.post("/api/authors", status_code=201)
async def create_author_view(data: Annotated[Authorcreate, Query()]):
    db = next(get_db())

    author = create_author(
        db=db,
        first_name=data.first_name,
        last_name=data.last_name,
        bio=data.bio,
        born_date=data.born_date,
    )

    response = data.model_dump()
    response["is_created"] = True

    return response
