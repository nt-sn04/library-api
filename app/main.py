from fastapi import FastAPI

from app.database import engine, Base
from app.models import *
from app.routers.authors import router as authors_router


Base.metadata.create_all(engine)

app = FastAPI(title="Library API")

app.include_router(authors_router)
