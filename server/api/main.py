from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends

from .routes.auth.auth_router import user_router
from .routes.books.books_router import book_router
from .security import get_current_user
from .. import User
from ..controller.db.db_provider import init_db

@asynccontextmanager
async def lifespan(_app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(user_router, prefix="/auth", tags=["auth"])
app.include_router(book_router, prefix="/books", tags=["books"])


@app.get("/", tags=["root"])
async def root(current_user: Annotated[User, Depends(get_current_user)]):
    return {"message": f"Welcome to your book collector {current_user.email}!"}
