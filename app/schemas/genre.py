from pydantic import BaseModel, ConfigDict, Field


class GenreResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class GenreCreate(BaseModel):
    name: str = Field(max_length=100)
    description: str | None = None


class GenreUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    description: str | None = None